# Week 1 · Exercise 4 — Zero trust as code

Zero trust: no access granted from network location alone; every request evaluated on identity + device + context. Default deny. Assume breach.

Files: [`zt_policy.py`](zt_policy.py) (PDP) · [`aaa_app.py`](aaa_app.py) (PEP + PIP) · [`zt_test.py`](zt_test.py)

Mode: security review of code with planted flaws, then fixed. Score **7/10** · tests **18 passed** (7 AAA + 11 zero trust).

## Design
| Component | Role | Where |
|---|---|---|
| PDP — Policy Decision Point | `decide(ctx) -> Decision`, pure function | `zt_policy.py` |
| PEP — Policy Enforcement Point | `zero_trust` FastAPI dependency; 403 "Access denied" | `aaa_app.py` |
| PIP — Policy Information Point | `USER_SECURITY` (MFA, device), `GEO_IP`, `ROUTE_POLICY`, clock | `aaa_app.py` |

## Rules (evaluated in order)
| # | Rule | Deny reason |
|---|---|---|
| 1 | User must be known | unknown user |
| 2 | Country in allow-list (CA, US) | country not allowed |
| 3 | Sensitivity/action must be known values | unknown sensitivity or action |
| 4 | High sensitivity → MFA **and** managed device | needs MFA and managed device |
| 5 | Admin action → admin role, 07:00 ≤ hour < 20:00 UTC | admin role / outside hours |
| 6 | Read → allow | — |
| 7 | Anything else | **default deny** |

## Flaws found and fixed
| Flaw | Fix |
|---|---|
| Final `return allow` | Default deny |
| Blocked-country list | Allow-list |
| MFA **or** managed device | MFA **and** managed device |
| `datetime.now()` inside `decide` | `ctx.hour` injected (pure, testable) |
| `7 <= h <= 20` | `7 <= h < 20` |
| Country from client header, default `"CA"` | Geo-IP from connection; unknown → deny |
| Unmapped route defaulted to low/read | 403 |
| `device_managed` from client header | Server-side PIP lookup |
| Deny reason returned to client | Generic "Access denied"; reason in `audit.log` only |

## Control labels
- `decide()` — Technical / Preventive (PDP)
- `zero_trust` dependency — Technical / Preventive (PEP)
- `USER_SECURITY` + geo-IP — PIP (supplies facts, not a control by itself)

## Open issues (next pass)
- [ ] PEP is per-route `Depends(zero_trust)` → a new route without it is open. Use `FastAPI(dependencies=[Depends(zero_trust)])` + explicit exemptions (`/health`)
- [ ] `request.client.host` behind a proxy (Railway/Cloudflare) = proxy IP. Use `CF-IPCountry` / `X-Forwarded-For` only from known proxy IPs; lock origin to Cloudflare
- [ ] `mfa_passed` is static per user; real MFA is per-session with freshness (e.g. ≤ 12 h)
- [ ] Remove commented flawed code → before/after note
- [ ] 10-min rebuild: rewrite `decide()` from a blank file

## Explain zero trust in 5 sentences — without the word "trust"
_TODO — write it (score was 0.5/1; needed for interviews + M1 video)._

## Weak spots
- Trusting client-controlled signals (headers)
- Fail-open default values (`"CA"` default, unmapped route → low)
- Defining zero trust crisply: verify every request explicitly, least privilege, assume breach
