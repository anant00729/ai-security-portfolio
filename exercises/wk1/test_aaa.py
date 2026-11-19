# exercises/wk1/test_aaa.py
import os
os.environ["VIEWER_KEY"] = "test-viewer-key"
os.environ["ADMIN_KEY"] = "test-admin-key"
from aaa_app import app, get_hour

import json
import pytest
from fastapi.testclient import TestClient
from aaa_app import app

client = TestClient(app)
VIEWER = {"X-API-Key": "test-viewer-key"}
ADMIN = {"X-API-Key": "test-admin-key"}
LOG = "audit.log"


@pytest.fixture(autouse=True)
def clean_log():
    if os.path.exists(LOG):
        os.remove(LOG)
    yield


def read_log():
    if not os.path.exists(LOG):
        return []
    with open(LOG) as f:
        return [json.loads(line) for line in f if line.strip()]


def test_no_key_401():
    assert client.get("/reports").status_code == 401

def test_bad_key_401():
    assert client.get("/reports", headers={"X-API-Key": "wrong"}).status_code == 401

def test_viewer_get_200():
    assert client.get("/reports", headers=VIEWER).status_code == 200

def test_viewer_delete_403():
    assert client.delete("/reports/2", headers=VIEWER).status_code == 403

def test_admin_delete_200():
    app.dependency_overrides[get_hour] = lambda: 10
    try:
        assert client.delete("/reports/1", headers=ADMIN).status_code == 200
    finally:
        app.dependency_overrides.clear()
        
def test_denied_request_is_logged():
    client.get("/reports")
    assert any(e["decision"] == "denied" for e in read_log())

def test_key_not_in_log():
    client.get("/reports", headers=VIEWER)
    with open(LOG) as f:
        assert "test-viewer-key" not in f.read()