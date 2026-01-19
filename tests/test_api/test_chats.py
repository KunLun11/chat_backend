import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_create_chat(client):
    response = client.post("/chats/", json={"title": "Test Chat"})
    assert response.status_code == 201


def test_create_chat_empty_title(client):
    response = client.post("/chats/", json={"title": ""})
    assert response.status_code == 400
