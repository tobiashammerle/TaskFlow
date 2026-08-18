from uuid import uuid4

import pytest

from taskflow.application.complete_task import CompleteTask
from taskflow.exceptions import TaskNotFoundError
from taskflow.task import Task
from tests.fakes import FakeTaskRepository


def test_complete_task_marks_task_as_completed():
    repository = FakeTaskRepository()
    complete_task = CompleteTask(repository)
    task = Task("Test Task")
    repository.add(task)
    complete_task.execute(task.id)
    updated_task = repository.get_by_id(task.id)
    assert updated_task.completed is True


def test_complete_task_raises_error_when_task_not_found():
    repository = FakeTaskRepository()
    complete_task = CompleteTask(repository)
    with pytest.raises(TaskNotFoundError):
        complete_task.execute(uuid4())
