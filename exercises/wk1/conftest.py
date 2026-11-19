# Shared test env: set before any test module imports aaa_app.
import os

os.environ.setdefault("VIEWER_KEY", "test-viewer-key")
os.environ.setdefault("ADMIN_KEY", "test-admin-key")
os.environ.setdefault("HONEYTOKEN", "AKIA-CANARY-7f3k9q2m")
