from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from taskflow.api import app
from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.filter_tasks import FilterTasks
from taskflow.application.get_tasks import GetTasks
from taskflow.application.remove_task import RemoveTask
from taskflow.application.search_tasks import SearchTasks
from taskflow.application.sort_tasks import SortTasks
from taskflow.routers.dependencies import (
    get_complete_task_use_case,
    get_create_task_use_case,
    get_filter_tasks_use_case,
    get_get_tasks_use_case,
    get_remove_task_use_case,
    get_search_tasks_use_case,
)
from tests.fakes import FakeTaskRepository


@pytest.fixture
def client():
    test_repository = FakeTaskRepository()
    test_create_task_use_case = CreateTask(test_repository)
    test_get_tasks_use_case = GetTasks(test_repository)
    test_complete_task_use_case = CompleteTask(test_repository)
    test_remove_task_use_case = RemoveTask(test_repository)
    test_search_tasks_use_case = SearchTasks()
    test_filter_tasks_use_case = FilterTasks()
    test_sort_tasks_use_case = SortTasks()

    def override_get_create_task_use_case():
        return test_create_task_use_case

    def override_get_get_tasks_use_case():
        return test_get_tasks_use_case

    def override_get_complete_task_use_case():
        return test_complete_task_use_case

    def override_get_remove_task_use_case():
        return test_remove_task_use_case

    def override_get_search_tasks_use_case():
        return test_search_tasks_use_case

    def override_get_filter_tasks_use_case():
        return test_filter_tasks_use_case

    def override_get_sort_tasks_use_case():
        return test_sort_tasks_use_case

    app.dependency_overrides[get_create_task_use_case] = (
        override_get_create_task_use_case
    )
    app.dependency_overrides[get_get_tasks_use_case] = override_get_get_tasks_use_case

    app.dependency_overrides[get_complete_task_use_case] = (
        override_get_complete_task_use_case
    )

    app.dependency_overrides[get_remove_task_use_case] = (
        override_get_remove_task_use_case
    )

    app.dependency_overrides[get_search_tasks_use_case] = (
        override_get_search_tasks_use_case
    )

    app.dependency_overrides[get_filter_tasks_use_case] = (
        override_get_filter_tasks_use_case
    )

    app.dependency_overrides[override_get_sort_tasks_use_case] = (
        override_get_sort_tasks_use_case
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


def test_delete_task_returns_204(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Einkaufen"},
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_unknown_task_returns_404(client):
    unknown_task_id = uuid4()
    response = client.delete(f"/tasks/{unknown_task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task nicht gefunden."


def test_search_tasks_returns_matching_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Python lernen",
        },
    )
    response = client.get("/tasks?search=einkaufen")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Einkaufen"


def test_search_tasks_returns_empty_list_when_no_match(client):
    client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    response = client.get("/tasks?search=xyz")
    assert response.status_code == 200
    assert response.json() == []


def test_filter_tasks_returns_completed_tasks(client):
    first_response = client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    client.post("/tasks", json={"title": "Python lernen"})
    first_task_id = first_response.json()["id"]
    client.patch(f"/tasks/{first_task_id}/complete")
    response = client.get("/tasks?filter=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Einkaufen"
    assert data[0]["completed"] is True


def test_search_and_filter_returns_only_matching_completed_tasks(client):
    first_response = client.post("/tasks", json={"title": "Python lernen"})
    client.post(
        "/tasks",
        json={
            "title": "Python testen",
        },
    )
    third_response = client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    first_task_id = first_response.json()["id"]
    client.patch(f"/tasks/{first_task_id}/complete")
    third_task_id = third_response.json()["id"]
    client.patch(f"/tasks/{third_task_id}/complete")
    response = client.get("/tasks?search=Python&filter=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python lernen"
    assert data[0]["completed"] is True


def test_filter_tasks_returns_422_for_invalid_filter(client):
    response = client.get("/tasks?filter=banana")
    assert response.status_code == 422


def test_filter_tasks_returns_open_tasks(client):
    first_response = client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    client.post("/tasks", json={"title": "Python lernen"})
    first_task_id = first_response.json()["id"]
    client.patch(f"/tasks/{first_task_id}/complete")
    response = client.get("/tasks?filter=open")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python lernen"
    assert data[0]["completed"] is False


def test_sort_tasks_by_title(client):
    client.post("/tasks", json={"title": "Python lernen"})
    client.post("/tasks", json={"title": "Einkaufen"})
    response = client.get("/tasks?sort=title")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Einkaufen"
    assert data[1]["title"] == "Python lernen"


def test_sort_tasks_by_title_descending(client):
    client.post("/tasks", json={"title": "Einkaufen"})
    client.post("/tasks", json={"title": "Python lernen"})
    response = client.get("/tasks?sort=title&reverse=true")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Python lernen"
    assert data[1]["title"] == "Einkaufen"


def test_reverse_without_sort_returns_400(client):
    response = client.get("/tasks?reverse=true")
    assert response.status_code == 400


def test_invalid_reverse_returns_422(client):
    response = client.get("/tasks?sort=title&reverse=banana")
    assert response.status_code == 422


def test_invalid_sort_returns_422(client):
    response = client.get("/tasks?sort=banana")
    assert response.status_code == 422


def test_search_filter_and_sort_tasks(client):
    first_response = client.post(
        "/tasks",
        json={
            "title": "Python lernen",
        },
    )
    client.post(
        "/tasks",
        json={  #
            "title": "Python testen"
        },
    )
    third_response = client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    fourth_response = client.post(
        "/tasks",
        json={
            "title": "Python API bauen",
        },
    )
    first_task_id = first_response.json()["id"]
    third_task_id = third_response.json()["id"]
    fourth_task_id = fourth_response.json()["id"]
    client.patch(f"/tasks/{first_task_id}/complete")
    client.patch(f"/tasks/{third_task_id}/complete")
    client.patch(f"/tasks/{fourth_task_id}/complete")
    response = client.get("/tasks?search=python&filter=completed&sort=title")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Python API bauen"
    assert data[1]["title"] == "Python lernen"


def test_limit_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "Python lernen",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "API testen",
        },
    )
    response = client.get("/tasks?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_offset_tasks_skips_requested_amount(client):
    client.post(
        "/tasks",
        json={
            "title": "Python lernen",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "Einkaufen",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "API testen",
        },
    )
    response = client.get("/tasks?offset=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Einkaufen"
    assert data[1]["title"] == "API testen"


def test_limit_and_offset_return_correct_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "A",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "B",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "C",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "D",
        },
    )
    response = client.get("/tasks?limit=2&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "B"
    assert data[1]["title"] == "C"


def test_negative_limit_returns_422(client):
    response = client.get("/tasks?limit=-2")
    assert response.status_code == 422


def test_negative_offset_returns_422(client):
    response = client.get("/tasks?offset=-1")
    assert response.status_code == 422


def test_limit_zero_returns_empty_list(client):
    response = client.get("/tasks?limit=0")
    assert response.status_code == 200
    assert response.json() == []


def test_offset_beyond_tasks_returns_empty_list(client):
    client.post(
        "/tasks",
        json={
            "title": "A",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "B",
        },
    )
    response = client.get("/tasks?offset=10")
    assert response.status_code == 200
    assert response.json() == []


def test_sort_offset_and_limit_return_correct_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "D",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "B",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "A",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "C",
        },
    )
    response = client.get("/tasks?sort=title&offset=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "B"
    assert data[1]["title"] == "C"


def test_limit_larger_than_remaining_tasks_returns_remaining_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "A",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "B",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "C",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "D",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "E",
        },
    )
    response = client.get("/tasks?offset=3&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "D"
    assert data[1]["title"] == "E"
