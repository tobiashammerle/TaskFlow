from taskflow.application.get_tasks import GetTasks
from taskflow.task import Task
from tests.fakes import FakeTaskRepository


def test_get_tasks_use_case_gets_all_tasks_from_repository() -> None:
    repository = FakeTaskRepository()
    task_1 = Task("Task 1")
    task_2 = Task("Task 2")
    repository.add(task_1)
    repository.add(task_2)
    get_tasks_use_case = GetTasks(repository)
    tasks = get_tasks_use_case.execute()
    assert len(tasks) == 2
    assert tasks[0].title == task_1.title
    assert tasks[1].title == task_2.title
