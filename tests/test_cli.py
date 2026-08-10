from taskflow.cli import add_task, show_tasks, complete_task, remove_task, run_cli
from taskflow.exceptions import EmptyTitleError, TaskNotFoundError
from taskflow.task import Task
import pytest

def mock_inputs(monkeypatch, values: list[str]) -> None:
    inputs = iter(values)
    monkeypatch.setattr(
            "builtins.input",
            lambda _: next(inputs),
        )

class FakeTaskService:
    def __init__(self, tasks=None) -> None:
        self.added_title: str | None = None
        self.tasks = tasks or []
        self.completed_index: int| None = None
        self.removed_index: int | None = None
        

    def add_task(self, title: str) -> None:
        self.added_title = title

    def get_tasks(self) -> list:
        return self.tasks

    def complete_task(self, index: int) -> Task:
        self.completed_index = index
        return self.tasks[index]

    def remove_task(self, index: int) -> Task:
        self.removed_index = index
        return self.tasks[index]

class FakeFailingTaskService:
    def add_task(self, title: str) -> None:
        raise EmptyTitleError

class FakeFailingCompleteTaskService:
    def get_tasks(self) -> list[Task]:
        return [Task("Python lernen"), Task("Git lernen")]
    def complete_task(self, index: int) -> Task:
        raise TaskNotFoundError(f"Keine Aufgabe mit Index {index} gefunden.")

class FakeFailingRemoveTaskService:
    def get_tasks(self) -> list[Task]:
        return [Task("Python lernen"), Task("Git lernen")]
    def remove_task(self, index: int) -> Task:
        raise TaskNotFoundError(f"Keine Aufgabe mit Index {index} gefunden.")

@pytest.fixture
def service() -> FakeTaskService:
    return FakeTaskService()

@pytest.fixture
def service_with_tasks() -> FakeTaskService:
    return FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])


def test_add_task_passes_title_to_service(service, monkeypatch, capsys) -> None:
    mock_inputs(monkeypatch,["Python lernen"])
    add_task(service)
    captured = capsys.readouterr()
    assert service.added_title == "Python lernen"
    assert "Aufgabe wurde hinzugefügt." in captured.out

def test_add_task_print_error_for_empty_title(monkeypatch, capsys) -> None:
    service = FakeFailingTaskService()
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    add_task(service)

    captured = capsys.readouterr()
    assert "Der Titel darf nicht leer sein." in captured.out

def test_show_task_prints_message_when_no_tasks(service, capsys) -> None:
    show_tasks(service)
    captured = capsys.readouterr()
    assert "Es sind noch keine Aufgaben vorhanden." in captured.out

def test_show_tasks_prints_existing_tasks(service_with_tasks, capsys) -> None:
    #service = FakeTaskService(tasks = [Task("Python lernen"), Task("Git lernen")])
    show_tasks(service_with_tasks)
    captured = capsys.readouterr()
    assert "Python lernen" in captured.out
    assert "Git lernen" in captured.out

def test_complete_task_passes_correct_index_to_service(service_with_tasks, monkeypatch, capsys) -> None:
    #service = FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])
    mock_inputs(monkeypatch, ["2"])
    complete_task(service_with_tasks)
    captured = capsys.readouterr()
    assert service_with_tasks.completed_index == 1
    assert "Git lernen" in captured.out

def test_complete_task_prints_error_when_task_not_found(monkeypatch, capsys) -> None:
    service = FakeFailingCompleteTaskService()
    mock_inputs(monkeypatch, ["5"])
    complete_task(service)
    captured = capsys.readouterr()
    assert "Keine Aufgabe mit Index" in captured.out

def test_remove_task_passes_correct_index_to_service(service_with_tasks, monkeypatch, capsys):
    #service = FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])
    mock_inputs(monkeypatch, ["2"])
    remove_task(service_with_tasks)
    captured = capsys.readouterr()
    assert service_with_tasks.removed_index == 1
    assert 'Die Aufgabe "Git lernen" wurde gelöscht.' in captured.out

def test_remove_task_prints_error_when_task_not_found(monkeypatch, capsys):
    service = FakeFailingRemoveTaskService()
    mock_inputs(monkeypatch, ["3"])
    remove_task(service)
    captured = capsys.readouterr()
    assert "Keine Aufgabe mit Index" in captured.out

def test_run_cli_adds_task_and_exits(service, monkeypatch, capsys) -> None:
    mock_inputs(monkeypatch, ["1", "Python lernen", "5"])
    run_cli(service)
    captured = capsys.readouterr()
    assert service.added_title == "Python lernen"
    assert "TaskFlow wird beendet." in captured.out

def test_run_cli_prints_error_for_invalid_choice(service, monkeypatch, capsys) -> None:
    mock_inputs(monkeypatch, ["abc", "5"])
    run_cli(service)
    captured = capsys.readouterr()
    assert "Ungültige Auswahl." in captured.out
    assert "TaskFlow wird beendet." in captured.out

