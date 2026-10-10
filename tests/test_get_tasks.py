from uuid import uuid4

from taskflow.application.get_tasks import GetTasks
from taskflow.task import Task
from tests.fakes import FakeTaskRepository, FakeUnitOfWork


def test_get_tasks_use_case_gets_all_tasks_from_unit_of_work() -> None:
    owner_id = uuid4()
    repository = FakeTaskRepository()
    task_1 = Task("Task 1", owner_id=owner_id)
    task_2 = Task("Task 2", owner_id=owner_id)
    repository.add(task_1)
    repository.add(task_2)
    uow = FakeUnitOfWork(repository)
    get_tasks_use_case = GetTasks(uow)
    tasks = get_tasks_use_case.execute()
    assert len(tasks) == 2
    assert tasks[0].title == task_1.title
    assert tasks[1].title == task_2.title


def test_get_tasks_returns_only_tasks_of_owner() -> None:
    owner_id_1 = uuid4()
    owner_id_2 = uuid4()
    repository = FakeTaskRepository()
    task_1 = Task("Task 1", owner_id=owner_id_1)
    task_2 = Task("Task 2", owner_id=owner_id_2)
    repository.add(task_1)
    repository.add(task_2)
    uow = FakeUnitOfWork(repository)
    get_tasks_use_case = GetTasks(uow)
    tasks_owner_1 = get_tasks_use_case.execute(owner_id=owner_id_1)
    tasks_owner_2 = get_tasks_use_case.execute(owner_id=owner_id_2)
    assert len(tasks_owner_1) == 1
    assert tasks_owner_1[0].title == task_1.title
    assert len(tasks_owner_2) == 1
    assert tasks_owner_2[0].title == task_2.title
