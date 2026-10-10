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
    owner_id = uuid4()
    task = Task("Python lernen", owner_id=owner_id)
    repository.save([task])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is False


def test_save_and_get_all_completed_task(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id = uuid4()
    task = Task("Python lernen", owner_id=owner_id)
    task.complete()
    repository.save([task])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is True


def test_save_and_get_all_preserves_priority(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id = uuid4()
    tasks = [Task("Python lernen", owner_id=owner_id, priority=Priority.HIGH)]
    repository.save(tasks)
    loaded_tasks = repository.get_all()
    assert loaded_tasks[0].priority == Priority.HIGH


def test_save_and_load_multiple_tasks_preserves_order(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id = uuid4()
    first_task = Task("Python lernen", owner_id=owner_id)
    second_task = Task("Git lernen", owner_id=owner_id)
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
    owner_id = uuid4()
    repository.save([Task("Alte Aufgabe", owner_id=owner_id)])
    repository.save([Task("Neue Aufgabe", owner_id=owner_id)])
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
    owner_id = uuid4()
    due_date = date(2026, 8, 31)
    repository.save([Task("Steuererklärung", owner_id=owner_id, due_date=due_date)])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].due_date == due_date


def test_save_and_get_all_preserves_task_id(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id = uuid4()
    original = Task("Python lernen", owner_id=owner_id)
    repository.save([original])
    loaded_tasks = repository.get_all()
    assert loaded_tasks[0].id == original.id


def test_get_all_by_owner_returns_only_tasks_of_owner(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id_1 = uuid4()
    owner_id_2 = uuid4()
    task_1 = Task("Python lernen", owner_id=owner_id_1)
    task_2 = Task("Git lernen", owner_id=owner_id_2)
    repository.save([task_1, task_2])
    tasks_owner_1 = repository.get_all_by_owner(owner_id_1)
    tasks_owner_2 = repository.get_all_by_owner(owner_id_2)
    assert len(tasks_owner_1) == 1
    assert tasks_owner_1[0].title == "Python lernen"
    assert len(tasks_owner_2) == 1
    assert tasks_owner_2[0].title == "Git lernen"


def test_get_task_by_id_returns_matching_task(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id = uuid4()
    task_1 = Task("Python lernen", owner_id=owner_id)
    task_2 = Task("Git lernen", owner_id=owner_id)
    repository.save([task_1, task_2])
    result = repository.get_by_id(task_2.id)
    assert result is not None
    assert result.id == task_2.id
    assert result.title == "Git lernen"


def test_get_task_by_id_returns_none_for_unknown_id(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    owner_id = uuid4()
    task_1 = Task("Python lernen", owner_id=owner_id)
    task_2 = Task("Git lernen", owner_id=owner_id)
    repository.save([task_1, task_2])
    unknown_id = uuid4()
    result = repository.get_by_id(unknown_id)
    assert result is None


def test_add_persists_single_task(tmp_path: Path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")
    owner_id = uuid4()
    task = Task("Python lernen", owner_id=owner_id)
    repository.add(task)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.title == "Python lernen"


def test_update_persists_changes_to_task(tmp_path: Path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")
    owner_id = uuid4()
    task = Task("Python lernen", owner_id=owner_id)
    repository.add(task)
    task.title = "Python fortgeschritten"
    task.complete()
    repository.update(task)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == "Python fortgeschritten"
    assert loaded_task.completed is True


def test_delete_removes_task(tmp_path: Path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")
    owner_id = uuid4()
    task = Task("Python lernen", owner_id=owner_id)
    repository.add(task)
    repository.delete(task.id)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is None


def test_delete_unknown_task_id_does_not_raise_error(tmp_path: Path) -> None:
    repository = JsonTaskRepository(tmp_path / "tasks.json")
    owner_id = uuid4()
    task = Task("Python lernen", owner_id=owner_id)
    repository.add(task)
    unknown_id = uuid4()
    repository.delete(unknown_id)  # Should not raise an error
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == "Python lernen"
