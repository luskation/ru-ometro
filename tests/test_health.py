def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "dev"}


def test_health_returns_app_version(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "abc123")
    assert client.get("/health").json()["version"] == "abc123"
