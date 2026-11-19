# exercises/wk1/test_zt.py
import os
os.environ.setdefault("VIEWER_KEY", "test-viewer-key")
os.environ.setdefault("ADMIN_KEY", "test-admin-key")

import json
import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
import aaa_app
from aaa_app import app, get_hour, get_country, zero_trust

client = TestClient(app)
VIEWER = {"X-API-Key": "test-viewer-key"}   # alice: MFA yes, managed device no
ADMIN = {"X-API-Key": "test-admin-key"}     # bob: MFA yes, managed device yes
LOG = "audit.log"


# A route we deliberately leave OUT of ROUTE_POLICY
@app.get("/unmapped")
def unmapped(user: dict = Depends(zero_trust)):
    return {"ok": True}


@pytest.fixture(autouse=True)
def reset():
    if os.path.exists(LOG):
        os.remove(LOG)
    app.dependency_overrides[get_hour] = lambda: 10      # default: office hours
    app.dependency_overrides[get_country] = lambda: "CA"  # default: allowed country
    yield
    app.dependency_overrides.clear()


def read_log():
    with open(LOG) as f:
        return [json.loads(line) for line in f if line.strip()]


def test_high_sensitivity_without_mfa_403(monkeypatch):
    monkeypatch.setitem(aaa_app.USER_SECURITY, "bob",
                        {"mfa_passed": False, "device_managed": True})
    assert client.get("/reports/1", headers=ADMIN).status_code == 403

def test_unmanaged_device_high_sensitivity_403():
    assert client.get("/reports/1", headers=VIEWER).status_code == 403

def test_admin_delete_at_21_is_403():
    app.dependency_overrides[get_hour] = lambda: 21
    assert client.delete("/reports/2", headers=ADMIN).status_code == 403

def test_admin_delete_at_10_is_200():
    assert client.delete("/reports/3", headers=ADMIN).status_code == 200

@pytest.mark.parametrize("hour,expected", [(6, 403), (7, 200), (19, 200), (20, 403)])
def test_admin_hour_boundaries(hour, expected):
    app.dependency_overrides[get_hour] = lambda: hour
    assert client.delete("/reports/99", headers=ADMIN).status_code == expected

def test_disallowed_country_403():
    app.dependency_overrides[get_country] = lambda: "FR"
    assert client.get("/reports", headers=VIEWER).status_code == 403

def test_unmapped_route_403():
    assert client.get("/unmapped", headers=ADMIN).status_code == 403

def test_reason_in_log_not_in_response():
    r = client.get("/reports/1", headers=VIEWER)
    assert r.status_code == 403
    assert "managed device" not in r.text
    assert any("managed device" in (e["reason"] or "") for e in read_log())