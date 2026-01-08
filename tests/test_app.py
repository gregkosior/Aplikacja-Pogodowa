import os
from pathlib import Path
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def test_index_ok(client):
    rv = client.get("/")
    assert rv.status_code == 200

def test_health(client):
    rv = client.get("/_health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert "status" in data
