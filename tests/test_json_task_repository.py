import json
from pathlib import Path
import pytest

from taskflow.json_task_repository import JsonTaskRepository
from taskflow.task import Task

def test_load_returns_empty_list_when_file_does_not_exist(tmp_path: Path) -> None:
    file_path = tmp_path /"tasks.json"
    repository = JsonTaskRepository(file_path)
    tasks = repository.load()
    assert tasks == []

def test_save_and_load_open_task(tmp_path: Path) -> None:
    file_path = tmp_path /"tasks.json"
    repository = JsonTaskRepository(file_path)
    task = Task("Python lernen")
    repository.save([task])
    loaded_tasks = repository.load()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is False

def test_save_and_load_completed_task(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    task = Task("Python lernen")
    task.complete()
    repository.save([task])
    loaded_tasks = repository.load()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is True

def test_save_and_load_multiple_tasks_preserves_order(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    repository = JsonTaskRepository(file_path)
    first_task = Task("Python lernen")
    second_task = Task("Git lernen")
    second_task.complete()
    repository.save([first_task, second_task])
    loaded_tasks = repository.load()
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
    loaded_tasks = repository.load()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Neue Aufgabe"


def test_load_raises_error_for_invalid_json(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    file_path.write_text("Das ist kein gültiges JSON", encoding="utf-8")
    repository = JsonTaskRepository(file_path)
    with pytest.raises(json.JSONDecodeError):
        repository.load()
