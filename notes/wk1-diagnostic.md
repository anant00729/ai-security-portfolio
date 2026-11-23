# Week 1 · Exercise 8 — Diagnostic results (final)

Two tests: Claude diagnostic (40 Q) + gap review, then Professor Messer Practice Exam A (85 MCQ).

| Date | Test | Score |
|---|---|---|
| 2026-11-20 | Claude diagnostic, 40 Q | 25/40 = 62.5% (many correct answers were educated guesses) |
| 2026-11-21 | Messer Practice Exam A, A6–A90, tutor mode (PBQs A1–A5 not done) | 54/85 = 63.5% (1st half ~58%, 2nd half ~70%) |
| | **Combined** | **79/125 = 63.2%** |

## Combined domain scores

Weighted gap = (85 − my %) × domain weight. Higher = study first.

| Priority | Domain | Diagnostic | Exam A | Combined | Weight | Weighted gap |
|---|---|---|---|---|---|---|
| 1 | D5 Security program mgmt & oversight | 4/8 | 7/12 | 11/20 = 55% | 20% | 600 |
| 2 | D4 Security operations | 7/11 | 16/25 | 23/36 = 64% | 28% | 591 |
| 3 | D2 Threats, vulns & mitigations | 6/9 | 11/18 | 17/27 = 63% | 22% | 484 |
| 4 | D3 Security architecture | 5/7 | 10/15 | 15/22 = 68% | 18% | 303 |
| 5 | D1 General security concepts | 3/5 | 10/15 | 13/20 = 65% | 12% | 240 |

D5 is the weakest domain in both tests.

## Diagnostic gap review (taught first, then recall questions, no options) — 13/16

| Topic | Score | Notes |
|---|---|---|
| Risk maths (AV, EF, SLE = AV × EF, ARO, ALE = SLE × ARO) | 3/4 | 40% of $200k: said $20k, correct $80k |
| Risk responses | 2/4 | Called insurance "avoid" (it's transfer); called removing a feature "mitigate" (it's avoid) |
| Forensics (order of volatility, image, write blocker, hashing, chain of custody, legal hold) | 2/2 | |
| MFA factor counting | 2/2 | |
| DLP vs email auth (SPF, DKIM, DMARC) | 2/2 | |
| Network zones (screened subnet/DMZ, intranet, extranet, VLAN) | 2/2 | |

**Diagnostic gaps now closed (right in Exam A):** backout plan · MFA factor counting · DLP for card data · SPF/DKIM/DMARC roles · tabletop exercise · SLE · risk response "mitigate" · IR phases (containment/recovery)

## Exam A misses (31), by root cause

- **Never learned the term:** DMARC disposition · federation · MOA · MTBF (guessed right) · record-level encryption · journaling · MDM · 802.1X · discretionary access control · enumeration · blockchain ledger · SCAP · HSM vs TPM · SASE (guessed right) · PCI DSS compliance · passive reconnaissance
- **Confused two terms:** replay vs DDoS · race condition vs malicious update · hardening vs least privilege · COPE vs MDM · deterrent vs preventive · continuity of ops vs tabletop · XSS vs buffer overflow · on-path vs host firewall · keylogger vs brute force (traffic direction) · automation vs attestation · escalation vs CI
- **Misread BEST / clue words:** availability for emergency systems · OS policy vs UTM for USB · hybrid cloud mismatches · phishing campaign = user reports · zero trust PEP/PDP (built this in Ex4!)

## Rules to keep

| Pair | Rule |
|---|---|
| Hashing vs encryption | Hash proves it's unchanged; encryption hides it |
| IaaS vs PaaS | You manage the OS = IaaS; only your code = PaaS |
| Controller / processor / custodian | Decides / does the work / looks after it |
| MFA | Count factor **types** (know / have / are / where), not items |
| Maintenance window vs backout plan | **When** vs **how to undo** |
| Avoid / transfer / mitigate | Remove it = avoid; someone else pays = transfer; keep it + add controls = mitigate |
| Replay vs DDoS | Capture something real and reuse it = replay; crash from many sources = DDoS |
| SSO vs federation | One login inside the same org = SSO; another org's login = federation |
| Hardening vs least privilege | Hardening protects a system; least privilege limits a user |
| TPM vs HSM | TPM = one device's keys; HSM = keys for many servers, centrally |
| COPE/BYOD/CYOD vs MDM | The first three say who owns the device; MDM enforces the policy |
| Keylogger vs brute force | Traffic out to one external IP = data exfil (keylogger); many logins coming in = brute force |
| Reading logs | Left = source, right = destination |

## Plan for weeks 2–4

- **Most time:** D5 governance/risk/compliance (weakest in both tests), D4 ops (heaviest weight)
- **Less time:** D3 architecture, D1 general concepts
- **Teaching style:** overview + plain one-line term explanations first, then questions. Understanding over memorising (no rote re-tests)
- **Term coverage:** walk the official SY0-701 objectives PDF one domain at a time for terms not yet met
- **Readiness rule:** book the exam once 2 practice tests in a row are ≥ 85%

## Next

- [ ] PBQs A1–A5 on the study site
- [ ] Rules above + Exam A misses → Anki; acronym trainer 15 min/day

Extra: 114-term glossary from the diagnostic saved as a Claude Sheet ("Security+ Glossary").
