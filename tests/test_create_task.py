from datetime import date

import pytest

from taskflow.application.create_task import CreateTask
from taskflow.exceptions import DuplicateTaskError
from taskflow.priority import Priority
from taskflow.task import Task
from tests.fakes import FakeTaskRepository


def test_create_task():
    repository = FakeTaskRepository()
    create_task = CreateTask(repository)
    task = create_task.execute(title="Test Task")
    tasks = repository.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert task.title == "Test Task"


def test_create_task_with_priority_and_due_date():
    repository = FakeTaskRepository()
    create_task = CreateTask(repository)
    create_task.execute(
        title="Test Task", priority=Priority.HIGH, due_date=date(2026, 8, 31)
    )
    tasks = repository.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].priority == Priority.HIGH
    assert tasks[0].due_date == date(2026, 8, 31)


def test_create_task_raises_dublicate_task_error_for_existing_title():
    repository = FakeTaskRepository()
    repository.add(Task(title="Einkaufen"))
    create_task = CreateTask(repository)
    with pytest.raises(DuplicateTaskError):
        create_task.execute("einkaufen")
