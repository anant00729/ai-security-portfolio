# Week 1 · Exercise 6 — Threat actors & social engineering

Mode: analysis (all answers produced by me). Score **6/10** (red flags 2/3 · extra emails 1.5/2 · matching 1.5/3 · explanation 0.5/1 · quiz 0.5/1).

## Phishing email — red flags (8/8, with nudges)
```text
From: "Stripe Billing" <billing@stripe-payments-secure.com>
Reply-To: accounts@mailbox-verify.ru
Authentication-Results: spf=fail; dkim=none; dmarc=fail
Subject: URGENT: Your payouts are suspended — action required within 2 hours
Verify your account now: https://dashboard.stripe.com.verify-login.io/auth
```
1. Look-alike sender domain (not `stripe.com`)
2. Reply-To on a different domain (`.ru`)
3. SPF fail
4. No DKIM
5. DMARC fail
6. Urgency + threat (2 hours, "permanently closed")
7. Deceptive link — real domain is `verify-login.io`; `dashboard.stripe.com` is only a subdomain
8. Generic greeting

Influence principles: urgency, authority, fear.

## Extra emails
| Email | Verdict | Evidence / key check |
|---|---|---|
| Stripe payout notice (spf/dkim/dmarc pass, real domain) | Legit ✅ | No over-flagging |
| Vendor bank-change request from `northrnark.com` | BEC + typosquatting ✅ | Verify bank-detail changes out-of-band via a known phone number |

## Actor + vector matching
| # | Scenario | Actor | Motive | Vector |
|---|---|---|---|---|
| a | Contractor copies DB before leaving | Malicious insider | Money / revenge | Legitimate access |
| b | Hijacked npm package steals env vars | Organized crime | Money | Supply chain |
| c | Ransomware gang buys VPN creds | Organized crime | Money | Stolen credentials + remote access |
| d | Unapproved AI note-taker on sales calls | Shadow IT | Convenience | Unsanctioned SaaS (data leakage) |
| e | Gov-backed, hidden for months | Nation-state (APT) | Espionage | Spear phishing |
| f | DDoS + climate message | Hacktivist | Ideology | Public-facing service |
| g | Hacked Python blog | Organized crime / nation-state | Varies | Watering hole |
| h | Poisoned Hugging Face model | Organized crime | Money | Supply chain (+ typosquatting) |

### Vector rule — "how did they get in?"
| Victim… | Vector |
|---|---|
| installed/consumed something from a trusted source | Supply chain |
| visited a normally-used site that was compromised | Watering hole |
| was already allowed in (own permissions) | Insider / legitimate access |
| had their login used by an outsider | Stolen credentials |

## Why MFA doesn't fully stop phishing
AiTM proxy kits relay the login and steal the session cookie; MFA fatigue (push bombing) tricks users into approving; stolen session tokens bypass MFA entirely. Fix: phishing-resistant MFA — FIDO2 / passkeys (bound to the real domain).

## Open items
- [ ] 60-second term-recall drill (whaling, smishing/vishing, DKIM vs DMARC, motives, watering hole, shadow IT, FIDO2)

## Weak spots
- Vector distinctions: supply chain vs watering hole vs legit access vs stolen creds
- Term recall: whaling, smishing, DKIM, hacktivist
