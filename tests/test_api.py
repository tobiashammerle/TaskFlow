from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from taskflow.api import (
    app,
    get_complete_task_use_case,
    get_create_task_use_case,
    get_get_tasks_use_case,
)
from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.get_tasks import GetTasks
from tests.fakes import FakeTaskRepository


@pytest.fixture
def client():
    test_repository = FakeTaskRepository()
    test_create_task_use_case = CreateTask(test_repository)
    test_get_tasks_use_case = GetTasks(test_repository)
    test_complete_task_use_case = CompleteTask(test_repository)

    def override_get_create_task_use_case():
        return test_create_task_use_case

    def override_get_get_tasks_use_case():
        return test_get_tasks_use_case

    def override_get_complete_task_use_case():
        return test_complete_task_use_case

    app.dependency_overrides[get_create_task_use_case] = (
        override_get_create_task_use_case
    )
    app.dependency_overrides[get_get_tasks_use_case] = override_get_get_tasks_use_case

    app.dependency_overrides[get_complete_task_use_case] = (
        override_get_complete_task_use_case
    )

    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_task_returns_201(client):
    response = client.post(
        "/tasks",
        json={
            "title": "API Test",
            "priority": "MEDIUM",
            "due_date": "2026-09-03",
        },
    )
    data = response.json()
    assert data["title"] == "API Test"
    assert response.status_code == 201


def test_create_same_title_in_fresh_repository_returns_201(client):
    response = client.post(
        "/tasks",
        json={
            "title": "API Test",
            "priority": "MEDIUM",
            "due_date": "2026-09-03",
        },
    )

    assert response.status_code == 201


def test_create_duplicate_task_returns_409(client):
    task_data = {
        "title": "Einkaufen",
        "priority": "MEDIUM",
        "due_date": "2026-09-03",
    }
    first_response = client.post("/tasks", json=task_data)
    second_response = client.post("/tasks", json=task_data)
    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Eine Aufgabe mit diesem Titel existiert bereits."
    )


def test_create_task_with_invalid_priority_returns_422(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Test",
            "priority": "SUPER WICHTIG",
        },
    )
    assert response.status_code == 422


def test_create_task_without_title_returns_422(client):
    response = client.post(
        "/tasks",
        json={
            "priority": "MEDIUM",
        },
    )
    assert response.status_code == 422


def test_create_task_with_empty_string_returns_400(client):
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "priority": "MEDIUM",
        },
    )
    assert response.status_code == 400


def test_get_tasks_returns_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_returns_created_task(client):
    client.post(
        "/tasks",
        json={
            "title": "Backend lernen",
            "priority": "HIGH",
            "due_date": "2026-09-01",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Backend lernen"


def test_complete_task_returns_completed_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    task_id = create_response.json()["id"]
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_unknown_task_returns_404(client):
    unknown_task_id = uuid4()
    response = client.patch(f"/tasks/{unknown_task_id}/complete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task nicht gefunden."
