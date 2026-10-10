from uuid import uuid4

from taskflow.application.get_statistics import GetStatistics
from taskflow.priority import Priority
from taskflow.task import Task


def test_get_statistics_counts_total_completed_and_open_tasks() -> None:
    owner_id = uuid4()
    task_a = Task("Task A", owner_id=owner_id)
    task_b = Task("Task B", owner_id=owner_id)
    task_c = Task("Task C", owner_id=owner_id)
    task_a.completed = True
    tasks = [task_a, task_b, task_c]
    get_statistics = GetStatistics()
    statistics = get_statistics.execute(tasks)
    assert statistics.total_tasks == 3
    assert statistics.completed_tasks == 1
    assert statistics.open_tasks == 2


def test_get_statistics_counts_high_priority_tasks() -> None:
    owner_id = uuid4()
    task_a = Task("Task 1", owner_id=owner_id)
    task_b = Task("Task 2", owner_id=owner_id)
    task_c = Task("Task 3", owner_id=owner_id)
    task_a.priority = Priority.HIGH
    task_b.priority = Priority.HIGH
    task_c.priority = Priority.MEDIUM
    tasks = [task_a, task_b, task_c]
    get_statistics = GetStatistics()
    statistics = get_statistics.execute(tasks)
    assert statistics.high_priority_tasks == 2


def test_get_statistics_returns_zero_for_empty_task_list() -> None:
    tasks: list[Task] = []
    get_statistics = GetStatistics()
    statistics = get_statistics.execute(tasks)
    assert statistics.total_tasks == 0
    assert statistics.completed_tasks == 0
    assert statistics.open_tasks == 0
    assert statistics.high_priority_tasks == 0
