# Week 1 · Exercise 8 — Diagnostic results

**Date:** 2026-11-20 · **Test:** Claude diagnostic, 40 questions · **Score:** 62.5% (25/40)

> Many correct answers were educated guesses (recognition, not recall), so the true baseline is likely below 62.5%.

## Domain scores

Weighted gap = (85 − my %) × domain weight. Higher = study first.

| Priority | Domain | My % | Weight | Weighted gap |
|---|---|---|---|---|
| 1 | D5 Security program management & oversight | 50% (4/8) | 20% | 700 |
| 2 | D4 Security operations | 64% (7/11) | 28% | 588 |
| 3 | D2 Threats, vulnerabilities & mitigations | 67% (6/9) | 22% | 396 |
| 4 | D1 General security concepts | 60% (3/5) | 12% | 300 |
| 5 | D3 Security architecture | 71% (5/7) | 18% | 252 |

Small sample: D1 rests on 5 questions. Re-check with Messer Practice Exam A (90 Q).

## Root causes of wrong answers

- **Never learned:** Q6 OCSP · Q10 SLA · Q11 PaaS · Q14 data controller · Q20 risk transfer · Q25 backout plan · Q34 DLP · Q37 screened subnet · Q39 order of volatility · Q40 SLE
- **Confused two terms:** Q7 race condition vs replay · Q16 hashing vs encryption · Q38 counted MFA items instead of factor types
- **Misread "BEST":** Q28 default configuration · Q36 stronger password

## Confused pairs → rules

| Pair | Rule |
|---|---|
| Hashing vs encryption | Hash proves it's unchanged; encryption hides it |
| IaaS vs PaaS | You manage the OS = IaaS; only your code = PaaS |
| Controller / processor / custodian | Decides / does the work / looks after it |
| MFA | Count factor **types** (know / have / are / where), not items |
| Maintenance window vs backout plan | **When** vs **how to undo** |
| Avoid vs transfer | Risk removed = avoid; risk stays but someone else pays = transfer |
| Avoid vs mitigate | Remove the feature = avoid; keep it and add controls = mitigate |

## Top gap review (taught first, then recall questions, no options) — 13/16

| Topic | Score | Notes |
|---|---|---|
| Risk maths (AV, EF, SLE = AV × EF, ARO, ALE = SLE × ARO) | 3/4 | 40% of $200k: said $20k, correct $80k. Briefly read 3×/year as ARO 0.3, then corrected |
| Risk responses | 2/4 | Called insurance "avoid" (transfer); called removing a feature "mitigate" (avoid). Mitigate + accept right |
| Forensics (order of volatility, forensic image, write blocker, hashing, chain of custody, legal hold) | 2/2 | |
| MFA factor counting | 2/2 | |
| DLP vs email auth (SPF, DKIM, DMARC) | 2/2 | |
| Network zones (screened subnet/DMZ, intranet, extranet, VLAN) | 2/2 | |

**Still weak after review:** avoid vs transfer vs mitigate · percentage arithmetic under pressure.

## Plan for weeks 2–4

- **Most time:** week 4 GRC (D5 weakest) and week 3 ops/IR (D4 heaviest weight)
- **Less time:** architecture (D3 strongest)
- **Teaching style:** overview + plain one-line term explanations first, then questions (no unexplained acronym dumps)
- **Readiness rule:** book the exam once 2 practice tests in a row are ≥ 85%

## Next

- [ ] Messer Practice Exam A, timed (90 Q) — note which answers were guesses
- [ ] Merge both results into one weighted-gap table
- [ ] Confused-pair rules → Anki; acronym trainer 15 min/day

Extra: 114-term glossary from this diagnostic saved as a Claude Sheet ("Security+ Glossary").
