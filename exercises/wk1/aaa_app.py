# exercises/wk1/aaa_app.py
import os
import secrets
import datetime
import json
from fastapi import FastAPI, Depends, HTTPException, Header, Request


app = FastAPI()

API_KEYS = {
    os.environ["VIEWER_KEY"]: {"user": "alice", "role": "viewer"},
    os.environ["ADMIN_KEY"]: {"user": "bob", "role": "admin"},
}

REPORTS = {1: "Q1 report", 2: "Q2 report", 3: "Q3 report"}


def get_current_user(request: Request, x_api_key: str | None = Header(default=None)) -> dict:
    if x_api_key:
        for key, info in API_KEYS.items():
            if secrets.compare_digest(x_api_key, key):
                request.state.user = info["user"]
                return info
    raise HTTPException(status_code=401, detail="Invalid or missing API key")


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] == "admin":
        return user
    raise HTTPException(status_code=403, detail="Admins only")


# @app.middleware("http")
# async def audit(request: Request, call_next):
#     response = await call_next(request)
#     if response.status_code < 400:
#         user = getattr(request.state, "user", "anonymous")
#         line = (
#             f'{{"ts": "{datetime.datetime.now().isoformat()}", '
#             f'"user": "{user}", '
#             f'"key": "{request.headers.get("x-api-key")}", '
#             f'"method": "{request.method}", '
#             f'"path": "{request.url.path}", '
#             f'"status": {response.status_code}, '
#             f'"decision": "allowed"}}'
#         )
#         with open("audit.log", "a") as f:
#             f.write(line + "\n")
#     return response

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
    }
    with open("audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return response

@app.get("/reports")
def list_reports(user: dict = Depends(get_current_user)):
    return {"user": user["user"], "reports": REPORTS}


@app.get("/reports/{report_id}")
def get_report(report_id: int, user: dict = Depends(get_current_user)):
    return {"id": report_id, "report": REPORTS.get(report_id)}


@app.delete("/reports/{report_id}")
def delete_report(report_id: int, user: dict = Depends(require_admin)):
    REPORTS.pop(report_id, None)
    return {"deleted": report_id, "by": user["user"]}