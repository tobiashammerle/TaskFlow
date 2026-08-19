from uuid import uuid4

import pytest

from taskflow.application.remove_task import RemoveTask
from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from tests.fakes import FakeTaskRepository


def test_remove_task_deletes_task() -> None:
    repository = FakeTaskRepository()
    remove_task = RemoveTask(repository)
    task = Task("Test Task")
    repository.add(task)
    removed_task = remove_task.execute(task.id)
    tasks = repository.get_all()
    assert len(tasks) == 0
    assert removed_task.id == task.id


def test_remove_task_raises_error_when_task_not_found() -> None:
    repository = FakeTaskRepository()
    remove_task = RemoveTask(repository)
    unknown_task = uuid4()
    with pytest.raises(TaskNotFoundError):
        remove_task.execute(unknown_task)
