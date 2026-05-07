from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_data_requires_api_key():
    response = client.get("/data/1")
    assert response.status_code == 403


def test_payload_validation_rejects_large_payload():
    response = client.post(
        "/data",
        headers={"X-API-Key": "mysecretkey"},
        json={"user_id": "1", "payload": "a" * 1500},
    )
    assert response.status_code == 422