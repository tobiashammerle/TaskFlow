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


class FakeCreateTask:
    def __init__(self) -> None:
        self.added_title: str | None = None

    def execute(self, title: str) -> None:
        if not title:
            raise EmptyTitleError
        self.added_title = title


class FakeCompleteTask:
    def __init__(self) -> None:
        self.completed_task_id = None

    def execute(self, task_id) -> None:
        self.completed_task_id = task_id


class FakeRemoveTask:
    def __init__(self) -> None:
        self.removed_task_id = None

    def execute(self, task_id) -> Task:
        self.removed_task_id = task_id
        return Task("Git lernen")


class FakeTaskService:
    def __init__(self, tasks=None) -> None:
        self.added_title: str | None = None
        self.tasks = tasks or []
        self.completed_task_id: UUID | None = None
        self.removed_task_id: UUID | None = None

    def add_task(self, title: str) -> None:
        self.added_title = title

    def get_tasks(self) -> list:
        return self.tasks

    def complete_task(self, task_id: UUID) -> Task:
        self.completed_task_id = task_id
        return next(task for task in self.tasks if task.id == task_id)

    def remove_task(self, task_id: UUID) -> Task:
        self.removed_task_id = task_id
        return next(task for task in self.tasks if task.id == task_id)


class FakeFailingTaskService:
    def add_task(self, title: str) -> None:
        raise EmptyTitleError


class FakeFailingCompleteTaskService:
    def __init__(self) -> None:
        self.tasks = [Task("Python lernen"), Task("Git lernen")]

    def get_tasks(self) -> list[Task]:
        return self.tasks

    def complete_task(self, task_id: UUID) -> Task:
        raise TaskNotFoundError(f"Keine Aufgabe mit ID {task_id} gefunden.")


class FakeFailingCompleteTask:
    def execute(self, task_id) -> None:
        raise TaskNotFoundError(f"Keine Aufgabe mit ID {task_id} gefunden.")


class FakeFailingRemoveTask:
    def execute(self, task_id):
        raise TaskNotFoundError(f"Keine Aufgabe mit ID {task_id} gefunden.")


class FakeFailingRemoveTaskService:
    def __init__(self) -> None:
        self.tasks = [Task("Python lernen"), Task("Git lernen")]

    def get_tasks(self) -> list[Task]:
        return self.tasks

    def remove_task(self, task_id: UUID) -> Task:
        raise TaskNotFoundError(f"Keine Aufgabe mit ID {task_id} gefunden.")


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
    create_task = FakeCreateTask()
    mock_inputs(monkeypatch, ["Python lernen"])
    add_task(create_task)
    captured = capsys.readouterr()
    assert create_task.added_title == "Python lernen"
    assert "Aufgabe wurde hinzugefügt." in captured.out


def test_add_task_print_error_for_empty_title(monkeypatch, capsys) -> None:
    create_task = FakeCreateTask()
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    add_task(create_task)

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


def test_complete_task_passes_correct_task_id_to_use_case(
    fake_service_with_tasks, monkeypatch, capsys
) -> None:
    complete_task_use_case = FakeCompleteTask()
    # service = FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])
    mock_inputs(monkeypatch, ["2"])
    complete_task(fake_service_with_tasks, complete_task_use_case)
    captured = capsys.readouterr()
    assert (
        complete_task_use_case.completed_task_id == fake_service_with_tasks.tasks[1].id
    )
    assert "Git lernen" in captured.out


def test_complete_task_prints_error_when_no_existing_tasks(capsys) -> None:
    service = FakeTaskService()
    complete_task_use_case = FakeCompleteTask()
    complete_task(service, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Es sind keine weiteren Aufgaben zum Erledigen vorhanden" in captured.out


def test_complete_task_prints_error_when_task_not_found(monkeypatch, capsys) -> None:
    service = FakeTaskService(tasks=[Task("Python lernen"), Task("Git lernen")])
    complete_task_use_case = FakeFailingCompleteTask()
    selected_task = service.get_tasks()[0]
    mock_inputs(monkeypatch, ["1"])
    complete_task(service, complete_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_remove_task_with_fake_service_removes_selected_task(
    fake_service_with_tasks, monkeypatch, capsys
):
    remove_task_use_case = FakeRemoveTask()
    selected_task = fake_service_with_tasks.tasks[1]
    mock_inputs(monkeypatch, ["2"])
    remove_task(fake_service_with_tasks, remove_task_use_case)
    captured = capsys.readouterr()
    assert remove_task_use_case.removed_task_id == selected_task.id
    assert 'Die Aufgabe "Git lernen" wurde gelöscht.' in captured.out


def test_remove_task_prints_error_when_no_existing_tasks(capsys) -> None:
    service = FakeTaskService()
    remove_task_use_case = FakeRemoveTask()
    remove_task(service, remove_task_use_case)
    captured = capsys.readouterr()
    assert "Es sind keine Aufgaben zum Löschen vorhanden." in captured.out


def test_remove_task_prints_error_when_task_not_found(monkeypatch, capsys):
    service = FakeFailingRemoveTaskService()
    selected_task = service.get_tasks()[0]
    remove_task_use_case = FakeFailingRemoveTask()
    mock_inputs(monkeypatch, ["1"])
    remove_task(service, remove_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_run_cli_adds_task_and_exits(service, monkeypatch, capsys) -> None:
    create_task = FakeCreateTask()
    complete_task_use_case = FakeCompleteTask()
    remove_task_use_case = FakeRemoveTask()
    mock_inputs(monkeypatch, ["1", "Python lernen", "5"])
    run_cli(service, create_task, complete_task_use_case, remove_task_use_case)
    assert create_task.added_title == "Python lernen"
    assert "TaskFlow wird beendet." in capsys.readouterr().out


def test_run_cli_prints_error_for_invalid_choice(service, monkeypatch, capsys) -> None:
    mock_inputs(monkeypatch, ["abc", "5"])
    create_task = FakeCreateTask()
    complete_task_use_case = FakeCompleteTask()
    remove_task_use_case = FakeRemoveTask()
    run_cli(service, create_task, complete_task_use_case, remove_task_use_case)
    captured = capsys.readouterr()
    assert "Ungültige Auswahl." in captured.out
    assert "TaskFlow wird beendet." in captured.out


def test_complete_task_calls_use_case_with_selected_task_id(
    mock_task_service, monkeypatch
) -> None:
    complete_task_use_case = FakeCompleteTask()
    task_1 = Task("Python lernen")
    task_2 = Task("Git üben")
    mock_task_service.get_tasks.return_value = [task_1, task_2]
    mock_task_service.complete_task.return_value = task_2
    mock_inputs(monkeypatch, ["2"])
    complete_task(mock_task_service, complete_task_use_case)
    assert complete_task_use_case.completed_task_id == task_2.id


def test_complete_task_prints_error_when_use_case_raises(
    mock_task_service, monkeypatch, capsys
) -> None:
    selected_task = mock_task_service.get_tasks.return_value[0]
    complete_task_use_case = FakeFailingCompleteTask()
    mock_inputs(monkeypatch, ["1"])
    complete_task(mock_task_service, complete_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_complete_task_does_not_call_use_case_for_invalid_input(
    mock_task_service, monkeypatch, capsys
) -> None:
    complete_task_use_case = FakeCompleteTask()
    mock_inputs(monkeypatch, ["abc"])
    complete_task(mock_task_service, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    assert complete_task_use_case.completed_task_id is None


def test_complete_task_does_not_call_use_case_for_zero(
    mock_task_service, monkeypatch, capsys
) -> None:
    complete_task_use_case = FakeCompleteTask()
    mock_inputs(monkeypatch, ["0"])
    complete_task(mock_task_service, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    assert complete_task_use_case.completed_task_id is None


def test_complete_task_does_not_call_use_case_for_number_out_of_range(
    mock_task_service, monkeypatch, capsys
) -> None:
    complete_task_use_case = FakeCompleteTask()
    mock_inputs(monkeypatch, ["99"])
    complete_task(mock_task_service, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    assert complete_task_use_case.completed_task_id is None


def test_remove_task_passes_correct_task_id_to_use_case(
    mock_task_service, monkeypatch
) -> None:
    remove_task_use_case = FakeRemoveTask()
    selected_task = mock_task_service.get_tasks.return_value[1]
    mock_task_service.remove_task.return_value = selected_task
    mock_inputs(monkeypatch, ["2"])
    remove_task(mock_task_service, remove_task_use_case)
    assert remove_task_use_case.removed_task_id == selected_task.id


def test_remove_task_does_not_call_use_case_for_invalid_input(
    mock_task_service, monkeypatch, capsys
) -> None:
    remove_task_use_case = FakeRemoveTask()
    mock_inputs(monkeypatch, ["abc"])
    remove_task(mock_task_service, remove_task_use_case)
    captured = capsys.readouterr()
    assert "Gib eine gültige Zahl ein." in captured.out
    assert remove_task_use_case.removed_task_id is None


def test_remove_task_prints_error_when_use_case_raises(
    mock_task_service, monkeypatch, capsys
) -> None:
    selected_task = mock_task_service.get_tasks.return_value[0]
    remove_task_use_case = FakeFailingRemoveTask()
    mock_inputs(monkeypatch, ["1"])
    remove_task(mock_task_service, remove_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out
