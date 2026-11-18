# Week 1 · Exercise 2 — CIA triad on a real project

Project: citizenquiz — Django API + Postgres + React frontend, Stripe payments, hosted on Railway behind Cloudflare.

## Assets (score 8/10)

| Asset | Most important | Threat | Actor + motive | Existing control |
|---|---|---|---|---|
| Django API | Availability — down = no practice or payments | Request flood (DDoS) | Unskilled attacker, fun/bragging | Cloudflare proxy (Technical / Preventive) |
| Postgres user DB | Confidentiality — user personal data | SQL injection dumps users table | Unskilled attacker, bragging | Django ORM parameterised queries (Technical / Preventive) |
| Stripe secret key | Confidentiality — leak = fraudulent charges | `.env` committed, scraped from Git history | Organised crime, money (careless insider causes leak) | Server-only `.env`, git-ignored (Technical / Preventive) |

## Gap
Weakest: Stripe key — single, human-dependent layer.
Add: pre-commit secret scanner (gitleaks) or GitHub push protection (Technical / Preventive).
Stronger: Stripe **restricted key** with only needed permissions (least privilege, Technical / Preventive).

## Review findings
- **All 3 controls are Preventive** — no Detective or Corrective layer. Assume preventive fails.

| Asset | Add Detective | Add Corrective |
|---|---|---|
| Django API | Uptime / error-rate alert | Rollback to last good deploy |
| Postgres DB | Alert on unusual query volume / bulk export | Backups + tested restore |
| Stripe key | Stripe alerts on unusual charges/refunds | Key-rotation runbook (revoke → reissue) |

- Non-repudiation: Django admin `LogEntry` (who did what); Stripe webhook signature verification (authenticity).

## To verify on the real app
- [ ] Railway origin URL not reachable directly (otherwise Cloudflare is bypassable)
- [ ] No raw SQL built from user input (`raw(`, `extra(`, `cursor()`)
- [ ] Backups exist and a restore has been tested

## Weak spots
- Backups are Corrective, not Preventive
- Least privilege enforced by IAM/roles = Technical (written as a principle in policy = Managerial)
- Controls that detect then block (IPS, WAF) = Preventive
- HTTPS protects Confidentiality/Integrity, not Availability
