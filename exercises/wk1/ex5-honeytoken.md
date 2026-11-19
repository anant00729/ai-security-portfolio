# Week 1 · Exercise 5 — Deception: honeytoken

Deception controls = fake assets no legitimate user should touch → any use is a high-confidence alert.
Honeypot (fake server) · honeynet (fake network) · honeyfile (fake doc) · **honeytoken** (fake credential/record).

Files: [`aaa_app.py`](aaa_app.py) (`check_honeytoken`) · [`config.example.env`](config.example.env) (the bait) · [`test_honeytoken.py`](test_honeytoken.py) · [`conftest.py`](conftest.py)

Mode: security review of code with planted flaws (rebuild skipped). Score **5.5/10** · flaws found **8/8** (some with hints) · tests **23 passed**.

## Design
- Bait: `AWS_ACCESS_KEY=AKIA-CANARY-...` "accidentally" left in `config.example.env` (committed on purpose; hyphens so it doesn't match a real AWS key pattern)
- Value loaded from env `HONEYTOKEN`; missing → app won't start (fail closed)
- Checked **first**, before normal auth; never grants access
- Use → identical generic 401 + `CRITICAL honeytoken_used` JSON event (UTC ts, source IP, user agent, method, path, key prefix)

## Flaws found and fixed
| # | Flaw | Fix |
|---|---|---|
| 1 | Revealing 401 ("incident reported") | Same generic 401 as any bad key |
| 2 | Checked after the login loop | Checked first |
| 3 | Honeytoken in `API_KEYS` (granted access) | Removed; loaded from env |
| 4 | `==` comparison | `secrets.compare_digest` |
| 5 | Source IP from `X-Forwarded-For` | `request.client.host` (or `CF-Connecting-IP` only behind locked-down Cloudflare) |
| 6 | f-string JSON | `json.dumps` (log injection) |
| 7 | Full key logged | Key prefix only |
| 8 | Level INFO | CRITICAL |

## Control label
Technical / **Detective** (Deterrent only if attackers know honeytokens are used). It blocks nothing — it reveals.

## Self-check
- ~Zero false positives: no legitimate user/process has any reason to use it
- Plant in: repo, CI/CD vars, wiki, S3 bucket, fake DB row, LLM system prompt / RAG docs
- On alert: page on-call, block source, **find how the bait was obtained — that's the real breach**

## Open issues
- [x] Tests failed from a clean shell (`KeyError: HONEYTOKEN`) → fixed with shared `conftest.py`
- [ ] 10-min rebuild: write `check_honeytoken()` + CRITICAL log from a blank file
- [ ] Remove commented flawed code → before/after note

## Weak spots
- Detective vs Preventive — honeytoken detects, doesn't block
- Response to the alert = hunt the entry point, not just the token use
