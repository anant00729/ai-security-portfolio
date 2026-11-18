# Week 1 · Exercise 1 — Classify security controls

Category = who/what enforces it (Technical · Managerial · Operational · Physical).
Type = what it does (Preventive · Detective · Corrective · Deterrent · Compensating · Directive).

## Part A — 10 controls (score 6.5/10)

| # | Control | My answer | Correct | Result |
|---|---|---|---|---|
| 1 | Login rate limiting | Technical / Preventive | Technical / Preventive | ✅ |
| 2 | Security camera | Physical / Detective | Physical / Detective (+ Deterrent) | ✅ |
| 3 | "Do not share passwords" policy | Managerial / Directive | Managerial / Directive | ✅ |
| 4 | Restore from backup after ransomware | Operational / Compensating | Operational or Technical / **Corrective** | ❌ |
| 5 | "Authorized personnel only" sign | Physical / Directive | Physical / Deterrent or Directive | ✅ |
| 6 | SIEM alert after 50 failed logins | Technical / Preventive | Technical / **Detective** | ⚠️ |
| 7 | Annual phishing training | Technical / Detective | **Operational / Preventive** | ❌ |
| 8 | Manual deploy approval (CI can't enforce) | Managerial / Compensating | **Operational** / Compensating | ⚠️ |
| 9 | Disk encryption | Technical / Preventive | Technical / Preventive | ✅ |
| 10 | Patching a vulnerable library | Operational / Preventive | **Technical / Corrective** (+ Preventive) | ⚠️ |

## Part B — controls in my own web app (score 4.5/6)

| Control | My answer | Correct |
|---|---|---|
| JWT auth | Technical / Preventive | ✅ |
| HTTPS | Technical / Preventive | ✅ |
| Input validation | Technical / Directive | ⚠️ Technical / **Preventive** |
| Database backups | Technical / Preventive | ⚠️ Technical / **Corrective** |
| Logging | Technical / Detective | ✅ |
| Rate limiting | Technical / Deterrent | ⚠️ Technical / **Preventive** (+ Deterrent) |

Missing types: Deterrent, Compensating, Directive. Detective present: yes (logging).

## Rules learned
1. **Who enforces it?** Software → Technical · document/decision → Managerial · people doing a process → Operational · physical thing → Physical.
2. **When does it act?** Blocks before → Preventive · only scares → Deterrent · notices during/after → Detective · repairs after → Corrective.
3. **Ignore test:** if the attacker ignores it and it still stops them → Preventive, not Deterrent/Directive.
4. Backups/restores/patching = Corrective. Alerts = Detective. Training = Operational.
5. Policy written = Managerial; people executing it = Operational.
