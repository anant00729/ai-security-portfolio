# exercises/wk1/aaa_app.py
import os
import json
import secrets
import datetime
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from zt_policy import Context, decide

app = FastAPI()

API_KEYS = {
    os.environ["VIEWER_KEY"]: {"user": "alice", "role": "viewer"},
    os.environ["ADMIN_KEY"]: {"user": "bob", "role": "admin"},
}

REPORTS = {1: "Q1 report", 2: "Q2 report", 3: "Q3 report"}

# PIP: server-side facts about each user
USER_SECURITY = {
    "alice": {"mfa_passed": True, "device_managed": False},
    "bob": {"mfa_passed": True, "device_managed": True},
}

# Server-side route -> policy map
ROUTE_POLICY = {
    ("GET", "/reports"): {"sensitivity": "low", "action": "read"},
    ("GET", "/reports/{report_id}"): {"sensitivity": "high", "action": "read"},
    ("DELETE", "/reports/{report_id}"): {"sensitivity": "high", "action": "admin"},
}

# Lab stand-in for a real geo-IP database (e.g. MaxMind)
GEO_IP = {"127.0.0.1": "CA", "testclient": "CA"}


def get_current_user(request: Request, x_api_key: str | None = Header(default=None)) -> dict:
    if x_api_key:
        for key, info in API_KEYS.items():
            if secrets.compare_digest(x_api_key, key):
                request.state.user = info["user"]
                return info
    raise HTTPException(status_code=401, detail="Invalid or missing API key")


# FLAWED: country taken from a client header, and missing header defaults to an allowed country
# def get_country(request: Request) -> str:
#     return request.headers.get("x-forwarded-country", "CA")


# FIX: country from the connection IP, unknown IP -> "UNKNOWN" (gets denied)
def get_country(request: Request) -> str:
    ip = request.client.host if request.client else ""
    return GEO_IP.get(ip, "UNKNOWN")


def get_hour() -> int:
    return datetime.datetime.now(datetime.timezone.utc).hour


# FLAWED: unmapped route defaults to low/read, device status from client header,
# and the exact deny reason is sent back to the client
# def zero_trust(
#     request: Request,
#     user: dict = Depends(get_current_user),
#     country: str = Depends(get_country),
#     hour: int = Depends(get_hour),
# ) -> dict:
#     route = request.scope["route"].path
#     policy = ROUTE_POLICY.get(
#         (request.method, route), {"sensitivity": "low", "action": "read"}
#     )
#     security = USER_SECURITY.get(user["user"], {})
#     ctx = Context(
#         user=user["user"],
#         role=user["role"],
#         mfa_passed=security.get("mfa_passed", False),
#         device_managed=request.headers.get("x-device-managed") == "true",
#         resource_sensitivity=policy["sensitivity"],
#         country=country,
#         hour=hour,
#         action=policy["action"],
#     )
#     decision = decide(ctx)
#     request.state.reason = decision.reason
#     if not decision.allow:
#         raise HTTPException(status_code=403, detail=decision.reason)
#     return user


# FIX: PEP with default deny, server-side signals only, generic message to client
def zero_trust(
    request: Request,
    user: dict = Depends(get_current_user),
    country: str = Depends(get_country),
    hour: int = Depends(get_hour),
) -> dict:
    route = request.scope["route"].path
    policy = ROUTE_POLICY.get((request.method, route))
    if policy is None:                                    # FIX 1: unmapped route -> deny
        request.state.reason = f"unmapped route {request.method} {route}"
        raise HTTPException(status_code=403, detail="Access denied")

    security = USER_SECURITY.get(user["user"], {})
    ctx = Context(
        user=user["user"],
        role=user["role"],
        mfa_passed=security.get("mfa_passed", False),
        device_managed=security.get("device_managed", False),  # FIX 2: server-side, not header
        resource_sensitivity=policy["sensitivity"],
        country=country,
        hour=hour,
        action=policy["action"],
    )
    decision = decide(ctx)
    request.state.reason = decision.reason               # real reason -> audit log only
    if not decision.allow:
        raise HTTPException(status_code=403, detail="Access denied")  # FIX 3: generic message
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