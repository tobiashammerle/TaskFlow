import sqlite3
from datetime import date
from pathlib import Path
from uuid import uuid4

import pytest

from taskflow.exceptions import RepositoryError
from taskflow.priority import Priority
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task import Task


def test_save_and_load_tasks(tmp_path: Path) -> None:
    database_path = tmp_path / "tasks.db"
    repository = SqliteTaskRepository(database_path)
    repository.initialize_database()
    first_task = Task(
        "Python lernen", priority=Priority.HIGH, due_date=date(2026, 8, 31)
    )
    second_task = Task("Git üben", priority=Priority.LOW)
    second_task.complete()
    repository.save([first_task, second_task])

    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Python lernen"
    assert loaded_tasks[0].completed is False
    assert loaded_tasks[0].priority == Priority.HIGH
    assert loaded_tasks[0].due_date == date(2026, 8, 31)
    assert loaded_tasks[1].title == "Git üben"
    assert loaded_tasks[1].completed is True
    assert loaded_tasks[1].priority == Priority.LOW
    assert loaded_tasks[1].due_date is None


def test_get_all_returns_empty_list_for_empty_database(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    loaded_tasks = repository.get_all()
    assert loaded_tasks == []


def test_save_overwrites_existing_tasks(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    repository.save([Task("Alte Aufgabe")])
    repository.save([Task("Neue Aufgabe")])
    loaded_tasks = repository.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Neue Aufgabe"


def test_save_and_get_all_preserves_task_id(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    original = Task("Python lernen")
    repository.save([original])
    loaded_tasks = repository.get_all()
    assert loaded_tasks[0].id == original.id


def test_get_by_id_returns_task_with_matching_id(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    task_1 = Task("Python lernen")
    task_2 = Task("Git üben")
    repository.save([task_1, task_2])

    loaded_task = repository.get_by_id(task_2.id)
    assert loaded_task is not None
    assert loaded_task.id == task_2.id
    assert loaded_task.title == "Git üben"


def test_get_by_id_returns_none_for_unknown_id(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    task = Task("Python lernen")
    repository.save([task])
    unknown_id = uuid4()
    loaded_task = repository.get_by_id(unknown_id)
    assert loaded_task is None


def test_add_persists_single_task(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    task = Task("Python lernen")
    repository.add(task)
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == "Python lernen"


def test_update_persists_changes_to_task(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    task = Task("Python lernen")
    repository.add(task)

    # Update the task's title and priority
    task.title = "Python fortgeschritten"
    task.priority = Priority.HIGH
    repository.update(task)

    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == "Python fortgeschritten"
    assert loaded_task.priority == Priority.HIGH


def test_delete_removes_task_from_database(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    task = Task("Python lernen")
    repository.add(task)

    # Delete the task
    repository.delete(task.id)

    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is None


def test_delete_unknown_id_does_not_raise_error(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    task = Task("Python lernen")
    repository.add(task)
    unknown_id = uuid4()
    repository.delete(unknown_id)  # Should not raise an error
    loaded_task = repository.get_by_id(task.id)
    assert loaded_task is not None
    assert loaded_task.id == task.id
    assert loaded_task.title == "Python lernen"


def test_delete_translates_sqlite_errors_to_repository_error(monkeypatch):
    repository = SqliteTaskRepository(Path("tasks.db"))

    def raise_sqlite_error(*args, **kwargs):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr(sqlite3, "connect", raise_sqlite_error)
    with pytest.raises(RepositoryError):
        repository.delete(uuid4())


def test_get_all_translates_sqlite_error_to_repository_error(monkeypatch):
    repository = SqliteTaskRepository(Path("tasks.db"))

    def raise_sqlite_error(*args, **kwargs):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr(sqlite3, "connect", raise_sqlite_error)
    with pytest.raises(RepositoryError):
        repository.get_all()
