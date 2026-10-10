from uuid import uuid4

import pytest

from taskflow.application.complete_task import CompleteTask
from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from tests.fakes import FakeTaskRepository, FakeUnitOfWork


def test_complete_task_marks_task_as_completed():
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    complete_task = CompleteTask(uow)
    task = Task("Test Task", owner_id=uuid4())
    repository.add(task)
    complete_task.execute(task.id)
    updated_task = repository.get_by_id(task.id)
    assert updated_task.completed is True


def test_complete_task_raises_error_when_task_not_found():
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    complete_task = CompleteTask(uow)
    with pytest.raises(TaskNotFoundError):
        complete_task.execute(uuid4())


def test_complete_task_of_other_owner_raises_task_not_found():
    owner_id = uuid4()
    other_owner_id = uuid4()
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    complete_task = CompleteTask(uow)
    task = Task("Fremde Aufgabe", owner_id=other_owner_id)
    repository.add(task)
    with pytest.raises(TaskNotFoundError):
        complete_task.execute(task.id, owner_id=owner_id)


def test_complete_task_of_owner_completes_task():
    owner_id = uuid4()
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    complete_task = CompleteTask(uow)
    task = Task("Eigene Aufgabe", owner_id=owner_id)
    repository.add(task)
    completed_task = complete_task.execute(task.id, owner_id=owner_id)
    assert completed_task.completed is True
