from pathlib import Path
from taskflow.sqlite_task_repository import SqliteTaskRepository
from taskflow.task_service import TaskService
from taskflow.cli import run_cli

def test_user_can_add_task_through_cli_and_persist_it(tmp_path: Path, monkeypatch) -> None:
    database_path = tmp_path /"test_tasks.db"
    repository = SqliteTaskRepository(database_path)
    repository.initialize_database()
    task_service = TaskService(repository)
    inputs = iter(["1", "Python lernen", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    run_cli(task_service)
    tasks = repository.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Python lernen"
def test_user_can_add_and_view_task_through_cli(tmp_path: Path, monkeypatch, capsys) -> None:
    database_path = tmp_path /"test_tasks.db"
    repository = SqliteTaskRepository(database_path)
    repository.initialize_database()
    task_service = TaskService(repository)
    inputs = iter(["1", "Python lernen", "2", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    run_cli(task_service)
    captured = capsys.readouterr()
    assert "Aufgabe wurde hinzugefügt." in captured.out
    assert "Python lernen" in captured.out
    
def test_user_can_complete_task_through_cli(tmp_path: Path, monkeypatch, capsys) -> None:
    database_path = tmp_path /"test_tasks.db"
    repository = SqliteTaskRepository(database_path)
    repository.initialize_database()
    task_service = TaskService(repository)
    inputs = iter(["1", "Python lernen", "3", "1", "2", "5"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )
    run_cli(task_service)
    captured = capsys.readouterr()
    assert "Aufgabe wurde hinzugefügt." in captured.out
    assert "Python lernen" in captured.out
    assert 'Aufgabe "Python lernen" wurde als erledigt markiert' in captured.out
    tasks = repository.get_all()
    assert tasks[0].completed is True
    