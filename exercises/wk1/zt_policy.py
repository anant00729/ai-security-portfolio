# exercises/wk1/zt_policy.py
from dataclasses import dataclass

KNOWN_USERS = {"alice", "bob"}
ALLOWED_COUNTRIES = {"CA", "US"}          # fix 2: allow-list, not block-list
KNOWN_SENSITIVITY = {"low", "high"}
KNOWN_ACTIONS = {"read", "admin"}


@dataclass(frozen=True)
class Context:
    user: str | None
    role: str
    mfa_passed: bool
    device_managed: bool
    resource_sensitivity: str  # "low" or "high"
    country: str
    hour: int  # 0-23, supplied by the caller
    action: str  # "read" or "admin"


@dataclass(frozen=True)
class Decision:
    allow: bool
    reason: str


def decide(ctx: Context) -> Decision:
    if ctx.user not in KNOWN_USERS:
        return Decision(False, "unknown user")

    if ctx.country not in ALLOWED_COUNTRIES:
        return Decision(False, f"country {ctx.country} not allowed")

    if ctx.resource_sensitivity not in KNOWN_SENSITIVITY or ctx.action not in KNOWN_ACTIONS:
        return Decision(False, "unknown sensitivity or action")

    if ctx.resource_sensitivity == "high":
        if not (ctx.mfa_passed and ctx.device_managed):   # fix 3: and, not or
            return Decision(False, "high sensitivity needs MFA and managed device")

    if ctx.action == "admin":
        if ctx.role != "admin":
            return Decision(False, "admin action needs admin role")
        if not (7 <= ctx.hour < 20):                      # fix 4 + 5: ctx.hour, end exclusive
            return Decision(False, "admin action outside 07:00-20:00")
        return Decision(True, "admin action allowed")

    if ctx.action == "read":
        return Decision(True, "read allowed")

    return Decision(False, "no rule matched")             # fix 1: default deny