from datetime import date
from pathlib import Path

from taskflow.priority import Priority
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task import Task

def test_save_and_load_tasks(tmp_path: Path) -> None:
    database_path = tmp_path / "tasks.db"
    repository = SqliteTaskRepository(database_path)
    repository.initialize_database()
    first_task = Task("Python lernen", priority=Priority.HIGH, due_date=date(2026, 8, 31))
    second_task = Task("Git üben", priority=Priority.LOW)
    second_task.complete()
    repository.save(
        [first_task,
        second_task]
    )

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

def test_load_returns_empty_list_for_empty_database(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    loaded_tasks = repository.load()
    assert loaded_tasks == []

def test_save_overwrites_existing_tasks(tmp_path: Path) -> None:
    repository = SqliteTaskRepository(tmp_path / "tasks.db")
    repository.initialize_database()
    repository.save([Task("Alte Aufgabe")])
    repository.save([Task("Neue Aufgabe")])
    loaded_tasks = repository.load()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Neue Aufgabe"


