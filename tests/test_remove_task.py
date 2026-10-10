from uuid import uuid4

import pytest

from taskflow.application.remove_task import RemoveTask
from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from tests.fakes import FakeTaskRepository, FakeUnitOfWork


def test_remove_task_deletes_task() -> None:
    owner_id = uuid4()
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    remove_task = RemoveTask(uow)
    task = Task("Test Task", owner_id=owner_id)
    repository.add(task)
    removed_task = remove_task.execute(task.id)
    tasks = repository.get_all()
    assert len(tasks) == 0
    assert removed_task.id == task.id


def test_remove_task_raises_error_when_task_not_found() -> None:
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    remove_task = RemoveTask(uow)
    unknown_task = uuid4()
    with pytest.raises(TaskNotFoundError):
        remove_task.execute(unknown_task)


def test_remove_task_of_other_owner_raises_task_not_found():
    owner_id = uuid4()
    other_owner_id = uuid4()
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    remove_task = RemoveTask(uow)
    task = Task("Fremde Aufgabe", owner_id=other_owner_id)
    repository.add(task)
    with pytest.raises(TaskNotFoundError):
        remove_task.execute(task.id, owner_id=owner_id)


def test_remove_task_of_owner_removes_task():
    owner_id = uuid4()
    repository = FakeTaskRepository()
    uow = FakeUnitOfWork(repository)
    remove_task = RemoveTask(uow)
    task = Task("Eigene Aufgabe", owner_id=owner_id)
    repository.add(task)
    remove_task.execute(task.id, owner_id=owner_id)
    assert repository.get_by_id(task.id) is None
