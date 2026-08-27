from datetime import date
from unittest.mock import Mock, create_autospec
from uuid import UUID

import pytest

from taskflow.cli import add_task, complete_task, remove_task, run_cli, show_tasks
from taskflow.exceptions import (
    DuplicateTaskError,
    EmptyTitleError,
    RepositoryError,
    TaskNotFoundError,
)
from taskflow.priority import Priority
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

    def execute(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> Task:
        if not title:
            raise EmptyTitleError
        self.added_title = title
        return Task(title=title, priority=priority, due_date=due_date)


class FakeCompleteTask:
    def __init__(self, task: Task | None = None) -> None:
        self.task: Task | None = task
        self.completed_task_id: UUID | None = None

    def execute(self, task_id: UUID) -> Task:
        self.completed_task_id = task_id
        if self.task is None:
            raise AssertionError("FakeCompleteTask wurde unerwartet ausgeführt.")
        return self.task


class FakeGetTasks:
    def __init__(self, tasks=None) -> None:
        self.tasks = tasks or []

    def execute(self) -> list[Task]:
        return self.tasks


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
    def execute(self, task_id: UUID) -> Task:
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


def test_show_task_prints_message_when_no_tasks(capsys) -> None:
    get_tasks_use_case = FakeGetTasks()
    show_tasks(get_tasks_use_case)
    captured = capsys.readouterr()
    assert "Es sind noch keine Aufgaben vorhanden." in captured.out


def test_show_tasks_prints_existing_tasks(capsys) -> None:
    get_tasks_use_case = FakeGetTasks([Task("Python lernen"), Task("Git lernen")])
    show_tasks(get_tasks_use_case)
    captured = capsys.readouterr()
    assert "Python lernen" in captured.out
    assert "Git lernen" in captured.out


def test_complete_task_passes_correct_task_id_to_use_case(monkeypatch, capsys) -> None:
    tasks = [Task("Python lernen"), Task("Git lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    complete_task_use_case = FakeCompleteTask(tasks[1])
    mock_inputs(monkeypatch, ["2"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert complete_task_use_case.completed_task_id == tasks[1].id
    assert "Git lernen" in captured.out


def test_complete_task_prints_error_when_no_existing_tasks(capsys) -> None:
    get_tasks_use_case = FakeGetTasks()
    complete_task_use_case = FakeCompleteTask()
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Es sind keine weiteren Aufgaben zum Erledigen vorhanden" in captured.out


def test_complete_task_prints_error_when_task_not_found(monkeypatch, capsys) -> None:
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    complete_task_use_case = FakeFailingCompleteTask()
    selected_task = tasks[0]
    mock_inputs(monkeypatch, ["1"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_remove_task_removes_selected_task(monkeypatch, capsys):
    tasks = [Task("Python lernen"), Task("Git lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    remove_task_use_case = FakeRemoveTask()
    selected_task = tasks[1]
    mock_inputs(monkeypatch, ["2"])
    remove_task(get_tasks_use_case, remove_task_use_case)
    captured = capsys.readouterr()
    assert remove_task_use_case.removed_task_id == selected_task.id
    assert 'Die Aufgabe "Git lernen" wurde gelöscht.' in captured.out


def test_remove_task_prints_error_when_no_existing_tasks(capsys) -> None:
    get_tasks_use_case = FakeGetTasks()
    remove_task_use_case = FakeRemoveTask()
    remove_task(get_tasks_use_case, remove_task_use_case)
    captured = capsys.readouterr()
    assert "Es sind keine Aufgaben zum Löschen vorhanden." in captured.out


def test_remove_task_prints_error_when_task_not_found(monkeypatch, capsys):
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    selected_task = tasks[0]
    remove_task_use_case = FakeFailingRemoveTask()
    mock_inputs(monkeypatch, ["1"])
    remove_task(get_tasks_use_case, remove_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_run_cli_adds_task_and_exits(monkeypatch, capsys) -> None:
    create_task = FakeCreateTask()
    complete_task_use_case = FakeCompleteTask()
    remove_task_use_case = FakeRemoveTask()
    get_tasks_use_case = FakeGetTasks()
    mock_inputs(monkeypatch, ["1", "Python lernen", "5"])
    run_cli(
        create_task, complete_task_use_case, remove_task_use_case, get_tasks_use_case
    )
    assert create_task.added_title == "Python lernen"
    assert "TaskFlow wird beendet." in capsys.readouterr().out


def test_run_cli_prints_error_for_invalid_choice(monkeypatch, capsys) -> None:
    mock_inputs(monkeypatch, ["abc", "5"])
    create_task = FakeCreateTask()
    complete_task_use_case = FakeCompleteTask()
    remove_task_use_case = FakeRemoveTask()
    get_tasks_use_case = FakeGetTasks()
    run_cli(
        create_task, complete_task_use_case, remove_task_use_case, get_tasks_use_case
    )
    captured = capsys.readouterr()
    assert "Ungültige Auswahl." in captured.out
    assert "TaskFlow wird beendet." in captured.out


def test_complete_task_calls_use_case_with_selected_task_id(monkeypatch) -> None:
    task_1 = Task("Python lernen")
    task_2 = Task("Git üben")
    tasks = [task_1, task_2]
    complete_task_use_case = FakeCompleteTask(task_2)
    get_tasks_use_case = FakeGetTasks(tasks)
    mock_inputs(monkeypatch, ["2"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    assert complete_task_use_case.completed_task_id == task_2.id


def test_complete_task_prints_error_when_use_case_raises(monkeypatch, capsys) -> None:
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    selected_task = tasks[0]
    complete_task_use_case = FakeFailingCompleteTask()
    mock_inputs(monkeypatch, ["1"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_complete_task_does_not_call_use_case_for_invalid_input(
    monkeypatch, capsys
) -> None:
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    complete_task_use_case = FakeCompleteTask()
    mock_inputs(monkeypatch, ["abc"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    assert complete_task_use_case.completed_task_id is None


def test_complete_task_does_not_call_use_case_for_zero(monkeypatch, capsys) -> None:
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    complete_task_use_case = FakeCompleteTask()
    mock_inputs(monkeypatch, ["0"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    assert complete_task_use_case.completed_task_id is None


def test_complete_task_does_not_call_use_case_for_number_out_of_range(
    monkeypatch, capsys
) -> None:
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    complete_task_use_case = FakeCompleteTask()
    mock_inputs(monkeypatch, ["99"])
    complete_task(get_tasks_use_case, complete_task_use_case)
    captured = capsys.readouterr()
    assert "Bitte gib eine gültige Zahl ein." in captured.out
    assert complete_task_use_case.completed_task_id is None


def test_remove_task_passes_correct_task_id_to_use_case(monkeypatch) -> None:
    tasks = [Task("Python lernen"), Task("Git lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    remove_task_use_case = FakeRemoveTask()
    selected_task = tasks[1]
    mock_inputs(monkeypatch, ["2"])
    remove_task(get_tasks_use_case, remove_task_use_case)
    assert remove_task_use_case.removed_task_id == selected_task.id


def test_remove_task_does_not_call_use_case_for_invalid_input(
    monkeypatch, capsys
) -> None:
    tasks = [Task("Python lernen"), Task("Git lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    remove_task_use_case = FakeRemoveTask()
    mock_inputs(monkeypatch, ["abc"])
    remove_task(get_tasks_use_case, remove_task_use_case)
    captured = capsys.readouterr()
    assert "Gib eine gültige Zahl ein." in captured.out
    assert remove_task_use_case.removed_task_id is None


def test_remove_task_prints_error_when_use_case_raises(monkeypatch, capsys) -> None:
    tasks = [Task("Python lernen")]
    get_tasks_use_case = FakeGetTasks(tasks)
    selected_task = tasks[0]
    remove_task_use_case = FakeFailingRemoveTask()
    mock_inputs(monkeypatch, ["1"])
    remove_task(get_tasks_use_case, remove_task_use_case)
    captured = capsys.readouterr()
    assert f"Keine Aufgabe mit ID {selected_task.id} gefunden." in captured.out


def test_run_cli_handles_repository_error(monkeypatch, capsys):
    create_task = Mock()
    complete_task = Mock()
    remove_task = Mock()
    get_tasks = Mock()

    get_tasks.execute.side_effect = RepositoryError(
        "Fehler beim Lesen der Aufgaben aus dem Repository."
    )

    inputs = iter(["2", "5"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_cli(
        create_task,
        complete_task,
        remove_task,
        get_tasks,
    )

    captured = capsys.readouterr()

    assert "Fehler beim Zugriff auf die Daten" in captured.out
    get_tasks.execute.assert_called_once_with()


def test_add_task_prints_error_for_duplicate_title(monkeypatch, capsys):
    create_task = Mock()
    create_task.execute.side_effect = DuplicateTaskError()

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Einkaufen",
    )

    add_task(create_task)

    captured = capsys.readouterr()

    assert "Eine Aufgabe mit diesem Titel existiert bereits." in captured.out
