from datetime import date
from uuid import uuid4

import pytest

from taskflow.application.create_task import CreateTask
from taskflow.exceptions import DuplicateTaskError
from taskflow.priority import Priority
from taskflow.task import Task
from tests.fakes import FakeTaskRepository, FakeUnitOfWork


def test_create_task():
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    create_task = CreateTask(uow)
    task = create_task.execute(title="Test Task", owner_id=uuid4())
    tasks = repository.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert task.title == "Test Task"


def test_create_task_with_priority_and_due_date():
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    create_task = CreateTask(uow)
    create_task.execute(
        title="Test Task",
        owner_id=uuid4(),
        priority=Priority.HIGH,
        due_date=date(2026, 8, 31),
    )
    tasks = repository.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].priority == Priority.HIGH
    assert tasks[0].due_date == date(2026, 8, 31)


def test_create_task_raises_dublicate_task_error_for_existing_title():
    owner_id = uuid4()
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    repository.add(Task(title="Einkaufen", owner_id=owner_id))
    create_task = CreateTask(uow)
    with pytest.raises(DuplicateTaskError):
        create_task.execute("einkaufen", owner_id=owner_id)
