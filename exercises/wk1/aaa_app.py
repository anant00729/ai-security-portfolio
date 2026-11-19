# exercises/wk1/aaa_app.py
import os
import json
import secrets
import datetime
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from zt_policy import Context, decide

app = FastAPI()

# FLAWED: honeytoken hard-coded in the source
# HONEYTOKEN = "AKIA-CANARY-7f3k9q2m"
# FIX: load from the real .env / environment, like other secrets
HONEYTOKEN = os.environ["HONEYTOKEN"]

API_KEYS = {
    os.environ["VIEWER_KEY"]: {"user": "alice", "role": "viewer"},
    os.environ["ADMIN_KEY"]: {"user": "bob", "role": "admin"},
    # FLAWED: honeytoken is a working login key
    # HONEYTOKEN: {"user": "svc-backup", "role": "viewer"},
    # FIX: removed - bait must never grant access
}

REPORTS = {1: "Q1 report", 2: "Q2 report", 3: "Q3 report"}

USER_SECURITY = {
    "alice": {"mfa_passed": True, "device_managed": False},
    "bob": {"mfa_passed": True, "device_managed": True},
}

ROUTE_POLICY = {
    ("GET", "/reports"): {"sensitivity": "low", "action": "read"},
    ("GET", "/reports/{report_id}"): {"sensitivity": "high", "action": "read"},
    ("DELETE", "/reports/{report_id}"): {"sensitivity": "high", "action": "admin"},
}

GEO_IP = {"127.0.0.1": "CA", "testclient": "CA"}

GENERIC_401 = "Invalid or missing API key"


def check_honeytoken(request: Request, key: str) -> bool:
    # FLAWED: == comparison leaks timing
    # if key == HONEYTOKEN:
    # FIX: constant-time comparison
    if not secrets.compare_digest(key, HONEYTOKEN):
        return False

    # FLAWED: IP from client-controlled header
    # ip = request.headers.get("x-forwarded-for", request.client.host)
    # FIX: IP from the real connection
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "")

    # FLAWED: f-string JSON (log injection), level INFO, full key logged
    # line = (
    #     f'{{"event": "honeytoken_used", "level": "INFO", '
    #     f'"ts": "{datetime.datetime.now(datetime.timezone.utc).isoformat()}", '
    #     f'"ip": "{ip}", "user_agent": "{ua}", "key": "{key}", '
    #     f'"method": "{request.method}", "path": "{request.url.path}"}}'
    # )
    # FIX: json.dumps escapes input, level CRITICAL, only a short key prefix
    entry = {
        "event": "honeytoken_used",
        "level": "CRITICAL",
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ip": ip,
        "user_agent": ua,
        "key_prefix": key[:9] + "...",
        "method": request.method,
        "path": request.url.path,
    }
    with open("audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return True


def get_current_user(request: Request, x_api_key: str | None = Header(default=None)) -> dict:
    # FLAWED: honeytoken checked AFTER the login loop, with a revealing message
    # if x_api_key:
    #     for key, info in API_KEYS.items():
    #         if secrets.compare_digest(x_api_key, key):
    #             request.state.user = info["user"]
    #             return info
    #     if check_honeytoken(request, x_api_key):
    #         raise HTTPException(status_code=401, detail="Invalid API key - this incident has been reported")
    # raise HTTPException(status_code=401, detail="Invalid or missing API key")

    # FIX: honeytoken checked FIRST, same 401 as any bad key
    if x_api_key:
        if check_honeytoken(request, x_api_key):
            raise HTTPException(status_code=401, detail=GENERIC_401)
        for key, info in API_KEYS.items():
            if secrets.compare_digest(x_api_key, key):
                request.state.user = info["user"]
                return info
    raise HTTPException(status_code=401, detail=GENERIC_401)


def get_country(request: Request) -> str:
    ip = request.client.host if request.client else ""
    return GEO_IP.get(ip, "UNKNOWN")


def get_hour() -> int:
    return datetime.datetime.now(datetime.timezone.utc).hour


def zero_trust(
    request: Request,
    user: dict = Depends(get_current_user),
    country: str = Depends(get_country),
    hour: int = Depends(get_hour),
) -> dict:
    route = request.scope["route"].path
    policy = ROUTE_POLICY.get((request.method, route))
    if policy is None:
        request.state.reason = f"unmapped route {request.method} {route}"
        raise HTTPException(status_code=403, detail="Access denied")

    security = USER_SECURITY.get(user["user"], {})
    ctx = Context(
        user=user["user"],
        role=user["role"],
        mfa_passed=security.get("mfa_passed", False),
        device_managed=security.get("device_managed", False),
        resource_sensitivity=policy["sensitivity"],
        country=country,
        hour=hour,
        action=policy["action"],
    )
    decision = decide(ctx)
    request.state.reason = decision.reason
    if not decision.allow:
        raise HTTPException(status_code=403, detail="Access denied")
    return user


@app.middleware("http")
async def audit(request: Request, call_next):
    response = await call_next(request)
    entry = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "user": getattr(request.state, "user", "anonymous"),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "decision": "denied" if response.status_code >= 400 else "allowed",
        "reason": getattr(request.state, "reason", None),
    }
    with open("audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return response


@app.get("/reports")
def list_reports(user: dict = Depends(zero_trust)):
    return {"user": user["user"], "reports": REPORTS}


@app.get("/reports/{report_id}")
def get_report(report_id: int, user: dict = Depends(zero_trust)):
    return {"id": report_id, "report": REPORTS.get(report_id)}


@app.delete("/reports/{report_id}")
def delete_report(report_id: int, user: dict = Depends(zero_trust)):
    REPORTS.pop(report_id, None)
    return {"deleted": report_id, "by": user["user"]}