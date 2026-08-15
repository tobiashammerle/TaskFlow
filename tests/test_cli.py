from unittest.mock import create_autospec
from uuid import UUID

import pytest

from taskflow.cli import add_task, complete_task, remove_task, run_cli, show_tasks
from taskflow.exceptions import EmptyTitleError, TaskNotFoundError
from taskflow.task import Task
from taskflow.task_service import TaskService


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
        self.completed_index: int | None = None
        self.removed_index: int | None = None

    def add_task(self, title: str) -> None:
        self.added_title = title

    def get_tasks(self) -> list:
        return self.tasks

    def complete_task(self, task_id: UUID) -> Task:
        self.completed_task_id = task_id
        return next(task for task in self.tasks if task.id == task_id)

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
def fake_service_with_tasks() -> FakeTaskService:
    return FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])


@pytest.fixture
def mock_task_service():
    service = create_autospec(TaskService, instance=True)
    service.get_tasks.return_value = [Task("Python lernen"), Task("Git üben")]
    return service


def test_add_task_passes_title_to_service(service, monkeypatch, capsys) -> None:
    mock_inputs(monkeypatch, ["Python lernen"])
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


def test_show_tasks_prints_existing_tasks(fake_service_with_tasks, capsys) -> None:
    # service = FakeTaskService(tasks = [Task("Python lernen"), Task("Git lernen")])
    show_tasks(fake_service_with_tasks)
    captured = capsys.readouterr()
    assert "Python lernen" in captured.out
    assert "Git lernen" in captured.out


def test_complete_task_passes_correct_task_id_to_service(
    fake_service_with_tasks, monkeypatch, capsys
) -> None:
    # service = FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])
    mock_inputs(monkeypatch, ["2"])
    complete_task(fake_service_with_tasks)
    captured = capsys.readouterr()
    assert (
        fake_service_with_tasks.completed_task_id == fake_service_with_tasks.tasks[1].id
    )
    assert "Git lernen" in captured.out


def test_complete_task_prints_error_when_no_existing_tasks(capsys) -> None:
    service = FakeTaskService()
    complete_task(service)
    captured = capsys.readouterr()
    assert "Es sind keine weiteren Aufgaben zum Erledigen vorhanden" in captured.out


def test_complete_task_prints_error_when_task_not_found(monkeypatch, capsys) -> None:
    service = FakeFailingCompleteTaskService()
    mock_inputs(monkeypatch, ["1"])
    complete_task(service)
    captured = capsys.readouterr()
    assert "Keine Aufgabe mit Index" in captured.out


def test_remove_task_with_fake_service_removes_selected_task(
    fake_service_with_tasks, monkeypatch, capsys
):
    # service = FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])
    mock_inputs(monkeypatch, ["2"])
    remove_task(fake_service_with_tasks)
    captured = capsys.readouterr()
    assert fake_service_with_tasks.removed_index == 1
    assert 'Die Aufgabe "Git lernen" wurde gelöscht.' in captured.out


def test_remove_task_prints_error_when_no_existing_tasks(capsys) -> None:
    service = FakeTaskService()
    remove_task(service)
    captured = capsys.readouterr()
    assert "Es sind keine Aufgaben zum Löschen vorhanden." in captured.out


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


def test_complete_task_calls_service_with_selected_task_id(
    mock_task_service, monkeypatch
) -> None:
    task_1 = Task("Python lernen")
    task_2 = Task("Git üben")
    mock_task_service.get_tasks.return_value = [task_1, task_2]
    mock_task_service.complete_task.return_value = task_2
    mock_inputs(monkeypatch, ["2"])
    complete_task(mock_task_service)
    mock_task_service.complete_task.assert_called_once_with(task_2.id)


def test_complete_task_prints_error_when_service_raises(
    mock_task_service, monkeypatch, capsys
) -> None:
    selected_task = mock_task_service.get_tasks.return_value[0]
    mock_task_service.complete_task.side_effect = TaskNotFoundError(
        f"Keine Aufgabe mit ID {selected_task.id} gefunden."
    )
    mock_inputs(monkeypatch, ["1"])
    complete_task(mock_task_service)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out
    mock_task_service.complete_task.assert_called_once_with(selected_task.id)


def test_complete_task_does_not_call_service_for_invalid_input(
    mock_task_service, monkeypatch, capsys
) -> None:
    mock_inputs(monkeypatch, ["abc"])
    complete_task(mock_task_service)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    mock_task_service.complete_task.assert_not_called()


def test_complete_task_does_not_call_service_for_zero(
    mock_task_service, monkeypatch, capsys
) -> None:
    mock_inputs(monkeypatch, ["0"])
    complete_task(mock_task_service)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    mock_task_service.complete_task.assert_not_called()


def test_complete_task_does_not_call_service_for_number_out_of_range(
    mock_task_service, monkeypatch, capsys
) -> None:
    mock_inputs(monkeypatch, ["99"])
    complete_task(mock_task_service)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    mock_task_service.complete_task.assert_not_called()


def test_remove_task_passes_correct_index_to_service(
    mock_task_service, monkeypatch
) -> None:
    mock_task_service.remove_task.return_value = Task("Git üben")
    mock_inputs(monkeypatch, ["2"])
    remove_task(mock_task_service)
    mock_task_service.remove_task.assert_called_once_with(1)


def test_remove_task_does_not_call_service_for_invalid_input(
    mock_task_service, monkeypatch, capsys
) -> None:
    mock_inputs(monkeypatch, ["abc"])
    remove_task(mock_task_service)
    captured = capsys.readouterr()
    assert "Gib eine gültige Zahl ein." in captured.out
    mock_task_service.remove_task.assert_not_called()


def test_remove_task_prints_error_when_service_raises(
    mock_task_service, monkeypatch, capsys
) -> None:
    mock_task_service.remove_task.side_effect = TaskNotFoundError(
        "Keine Aufgabe mit Index 4 gefunden."
    )
    mock_inputs(monkeypatch, ["5"])
    remove_task(mock_task_service)
    captured = capsys.readouterr()
    assert "Keine Aufgabe mit Index 4 gefunden." in captured.out
    mock_task_service.remove_task.assert_called_once_with(4)
