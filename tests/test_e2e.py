from pathlib import Path

import pytest

from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.get_tasks import GetTasks
from taskflow.application.remove_task import RemoveTask
from taskflow.cli import run_cli
from taskflow.repository_unit_of_work import RepositoryUnitOfWork
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task_service import TaskService


@pytest.fixture
def sqlite_repository(tmp_path: Path) -> SqliteTaskRepository:
    database = tmp_path / "test_tasks.db"
    repository = SqliteTaskRepository(database)
    repository.initialize_database()
    return repository


@pytest.fixture
def task_service(sqlite_repository) -> TaskService:
    uow = RepositoryUnitOfWork(sqlite_repository)
    return TaskService(uow)


def test_user_can_add_task_through_cli_and_persist_it(
    sqlite_repository, monkeypatch
) -> None:
    inputs = iter(["1", "Python lernen", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    uow = RepositoryUnitOfWork(sqlite_repository)
    create_task = CreateTask(uow)
    complete_task = CompleteTask(uow)
    remove_task = RemoveTask(uow)
    get_tasks_use_case = GetTasks(sqlite_repository)
    run_cli(create_task, complete_task, remove_task, get_tasks_use_case)
    tasks = sqlite_repository.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Python lernen"


def test_user_can_add_and_view_task_through_cli(
    sqlite_repository, monkeypatch, capsys
) -> None:
    inputs = iter(["1", "Python lernen", "2", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    uow = RepositoryUnitOfWork(sqlite_repository)
    create_task = CreateTask(uow)
    complete_task = CompleteTask(uow)
    remove_task = RemoveTask(uow)
    get_tasks_use_case = GetTasks(sqlite_repository)
    run_cli(create_task, complete_task, remove_task, get_tasks_use_case)
    captured = capsys.readouterr()
    assert "Aufgabe wurde hinzugefügt." in captured.out
    assert "Python lernen" in captured.out


def test_user_can_complete_task_through_cli(
    sqlite_repository, monkeypatch, capsys
) -> None:
    inputs = iter(["1", "Python lernen", "3", "1", "2", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    uow = RepositoryUnitOfWork(sqlite_repository)
    create_task = CreateTask(uow)
    complete_task = CompleteTask(uow)
    remove_task = RemoveTask(uow)
    get_tasks_use_case = GetTasks(sqlite_repository)
    run_cli(create_task, complete_task, remove_task, get_tasks_use_case)
    captured = capsys.readouterr()
    assert "Aufgabe wurde hinzugefügt." in captured.out
    assert "Python lernen" in captured.out
    assert 'Aufgabe "Python lernen" wurde als erledigt markiert' in captured.out
    tasks = sqlite_repository.get_all()
    assert tasks[0].completed is True


def test_user_can_remove_task_through_cli(
    sqlite_repository, monkeypatch, capsys
) -> None:
    inputs = iter(["1", "Python lernen", "4", "1", "2", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    uow = RepositoryUnitOfWork(sqlite_repository)
    create_task = CreateTask(uow)
    complete_task = CompleteTask(uow)
    remove_task = RemoveTask(uow)
    get_tasks_use_case = GetTasks(sqlite_repository)
    run_cli(create_task, complete_task, remove_task, get_tasks_use_case)
    captured = capsys.readouterr()
    assert "Aufgabe wurde hinzugefügt." in captured.out
    assert "Python lernen" in captured.out
    assert 'Die Aufgabe "Python lernen" wurde gelöscht.' in captured.out
    tasks = sqlite_repository.get_all()
    assert len(tasks) == 0
