import json
from datetime import date
from pathlib import Path
from uuid import uuid4

import pytest

from taskflow.json_task_repository import JsonTaskRepository
from taskflow.priority import Priority
from taskflow.task import Task


def test_get_all_returns_empty_list_when_file_does_not_exist(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    tasks = repository.get_all()
    assert tasks == []


def test_save_and_get_all_open_task(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    task = Task("Python lernen")
    repository.save([task])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is False


def test_save_and_get_all_completed_task(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    task = Task("Python lernen")
    task.complete()
    repository.save([task])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is True


def test_save_and_get_all_preserves_priority(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    tasks = [Task("Python lernen", priority=Priority.HIGH)]
    repository.save(tasks)
    loaded_tasks = repository.get_all()
    assert loaded_tasks[0].priority == Priority.HIGH


def test_save_and_load_multiple_tasks_preserves_order(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    first_task = Task("Python lernen")
    second_task = Task("Git lernen")
    second_task.complete()
    repository.save([first_task, second_task])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is False
    assert loaded_tasks[1].title == "Git lernen"
    assert loaded_tasks[1].completed is True


def test_save_overwrites_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    repository.save([Task("Alte Aufgabe")])
    repository.save([Task("Neue Aufgabe")])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Neue Aufgabe"


def test_get_all_raises_error_for_invalid_json(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    file_path.write_text("Das ist kein gültiges JSON", encoding="utf-8")
    repository = JsonTaskRepository(file_path)
    with pytest.raises(json.JSONDecodeError):
        repository.get_all()


def test_save_and_get_all_preserves_due_date(tmp_path: Path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")
    due_date = date(2026, 8, 31)
    repository.save([Task("Steuererklärung", due_date=due_date)])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].due_date == due_date


def test_save_and_get_all_preserves_task_id(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    original = Task("Python lernen")
    repository.save([original])
    loaded_tasks = repository.get_all()
    assert loaded_tasks[0].id == original.id


def test_get_task_by_id_returns_matching_task(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    task_1 = Task("Python lernen")
    task_2 = Task("Git lernen")
    repository.save([task_1, task_2])
    result = repository.get_by_id(task_2.id)
    assert result is not None
    assert result.id == task_2.id
    assert result.title == "Git lernen"


def test_get_task_by_id_returns_none_for_unknown_id(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    task_1 = Task("Python lernen")
    task_2 = Task("Git lernen")
    repository.save([task_1, task_2])
    unknown_id = uuid4()
    result = repository.get_by_id(unknown_id)
    assert result is None


def test_add_persists_single_task(tmp_path: Path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")
    task = Task("Python lernen")
    repository.add(task)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.title == "Python lernen"
