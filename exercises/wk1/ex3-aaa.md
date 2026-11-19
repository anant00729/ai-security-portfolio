# Week 1 · Exercise 3 — AAA in FastAPI

**AAA** = Authentication (who are you?) → Authorization (what may you do?) → Accounting (record what you did).

Files: [`aaa_app.py`](aaa_app.py) · [`test_aaa.py`](test_aaa.py)

Mode: security review of code with planted flaws, then fixed. Score **7.5/10** · tests **7 passed**.

## Run
```bash
python -m venv .venv && .venv/bin/pip install fastapi uvicorn pytest httpx
.venv/bin/pytest -q
```

## Flaws found and fixed
| Flaw | Risk | Fix |
|---|---|---|
| Unknown key → 403 | Leaks whether a key exists; wrong semantics | 401, same message as missing key |
| Key compared with `==` | Timing attack | `secrets.compare_digest` |
| Role read from client `X-Role` header | Privilege escalation | Role from server-side key mapping only |
| `GET /reports/{id}` had no auth dependency | FastAPI is default-allow | Added `Depends(get_current_user)` |
| Denied requests not logged (`< 400` filter) | Blind to attacks | Log every request |
| API key written to log | Secret leakage | Removed |
| f-string JSON | Log injection | `json.dumps` |
| Local time, no zone | Unreliable timeline | UTC ISO 8601 |

## Control labels
- API key check — Technical / Preventive
- Role check — Technical / Preventive
- Audit log — Technical / Detective

## Open issues (next pass)
- [ ] `decision` = denied only for 401/403 (not 404/422/500)
- [ ] Log in `try/finally` so crashing requests still get a line
- [ ] Store `sha256(key)` and do a direct lookup instead of looping `compare_digest`
- [ ] Move commented vulnerable middleware out to a before/after note
- [ ] Tests: same message for missing vs bad key; `GET /reports/{id}` without key → 401

## Weak spots
- Audit logs provide **accountability / non-repudiation** and detect violations; the log itself needs integrity (tamper-evidence) **and** confidentiality (may hold PII)
- Encryption ≠ tamper-evidence → SIEM shipping, append-only storage, hash chaining
- Category = who enforces it → code = Technical
