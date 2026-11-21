from fastapi.testclient import TestClient
from service.app import app


def test_health_and_metrics(monkeypatch):
    monkeypatch.delenv('DG_FAIL_READINESS', raising=False)
    with TestClient(app) as client:
        assert client.get('/healthz').status_code == 200
        assert client.get('/readyz').status_code == 200
        assert client.get('/metrics').status_code == 200
        assert b'http_requests_total' in client.get('/metrics').content


def test_failure_injection_only_affects_readiness(monkeypatch):
    monkeypatch.setenv('DG_FAIL_READINESS', '1')
    with TestClient(app) as client:
        assert client.get('/healthz').status_code == 200
        assert client.get('/readyz').status_code == 503
