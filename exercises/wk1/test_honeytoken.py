# exercises/wk1/test_honeytoken.py
import os
os.environ.setdefault("VIEWER_KEY", "test-viewer-key")
os.environ.setdefault("ADMIN_KEY", "test-admin-key")
os.environ.setdefault("HONEYTOKEN", "AKIA-CANARY-7f3k9q2m")

import json
import pytest
from fastapi.testclient import TestClient
from aaa_app import app

client = TestClient(app)
HONEY = {"X-API-Key": os.environ["HONEYTOKEN"]}
BAD = {"X-API-Key": "wrong-key"}
LOG = "audit.log"


@pytest.fixture(autouse=True)
def clean_log():
    if os.path.exists(LOG):
        os.remove(LOG)
    yield


def read_log():
    with open(LOG) as f:
        return [json.loads(line) for line in f if line.strip()]


def test_honeytoken_gets_401():
    assert client.get("/reports", headers=HONEY).status_code == 401

def test_honeytoken_response_same_as_bad_key():
    honey = client.get("/reports", headers=HONEY)
    bad = client.get("/reports", headers=BAD)
    assert honey.status_code == bad.status_code
    assert honey.json() == bad.json()
    assert honey.headers.get("content-type") == bad.headers.get("content-type")

def test_honeytoken_logs_critical_event():
    client.get("/reports", headers=HONEY)
    events = [e for e in read_log() if e.get("event") == "honeytoken_used"]
    assert len(events) == 1
    assert events[0]["level"] == "CRITICAL"

def test_full_honeytoken_not_in_log():
    client.get("/reports", headers=HONEY)
    with open(LOG) as f:
        assert os.environ["HONEYTOKEN"] not in f.read()

def test_bad_key_does_not_trigger_alarm():
    client.get("/reports", headers=BAD)
    assert not any(e.get("event") == "honeytoken_used" for e in read_log())