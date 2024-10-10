from fastapi.testclient import TestClient

from conftest import app

client = TestClient(app)

def test_get_foo():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": 'foo1'}