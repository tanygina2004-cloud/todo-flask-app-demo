import sys
import os
import tempfile
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from db import init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    app.config["TESTING"] = True
    app.config["DB_NAME"] = db_path
    init_db(db_path)
    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "Testing",
            "due_date": "2025-12-31",
            "status": "pending",
        },
    )

    assert response.status_code == 201
    assert response.json["message"] == "Task created"


def test_get_all_tasks(client):
    client.post(
        "/api/tasks",
        json={
            "title": "Task 1",
            "description": "",
            "due_date": "2025-12-31",
            "status": "pending",
        },
    )

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Task 1"


def test_get_task_by_id(client):
    client.post(
        "/api/tasks",
        json={
            "title": "Single Task",
            "description": "",
            "due_date": "2025-12-31",
            "status": "pending",
        },
    )

    response = client.get("/api/tasks/1")

    assert response.status_code == 200
    assert response.json["title"] == "Single Task"


def test_update_task(client):
    client.post(
        "/api/tasks",
        json={
            "title": "Old Title",
            "description": "",
            "due_date": "2025-12-31",
            "status": "pending",
        },
    )

    response = client.put("/api/tasks/1", json={"status": "completed"})

    assert response.status_code == 200
    assert response.json["message"] == "Task updated"


def test_delete_task(client):
    client.post(
        "/api/tasks",
        json={
            "title": "Delete Me",
            "description": "",
            "due_date": "2025-12-31",
            "status": "pending",
        },
    )

    response = client.delete("/api/tasks/1")

    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"
