from datetime import date

from taskflow.application.sort_tasks import SortTasks
from taskflow.priority import Priority
from taskflow.sort_field import SortField
from taskflow.task import Task
from tests.fakes import FakeTaskRepository


def test_sort_tasks_by_title_returns_tasks_in_alphabetical_order() -> None:
    repository = FakeTaskRepository()
    repository.add(Task("Python lernen"))
    repository.add(Task("Einkaufen"))
    repository.add(Task("Git lernen"))
    tasks = repository.get_all()
    sort_tasks_use_case = SortTasks()
    sorted_tasks = sort_tasks_use_case.execute(tasks, SortField.TITLE)
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].title == "Einkaufen"
    assert sorted_tasks[1].title == "Git lernen"
    assert sorted_tasks[2].title == "Python lernen"


def test_sort_tasks_by_priority_returns_highest_priority_first() -> None:
    repository = FakeTaskRepository()
    repository.add(Task("Einkaufen", Priority.LOW))
    repository.add(Task("Python lernen", Priority.HIGH))
    repository.add(Task("Git lernen", Priority.MEDIUM))
    tasks = repository.get_all()
    sorted_tasks_use_case = SortTasks()
    sorted_tasks = sorted_tasks_use_case.execute(tasks, SortField.PRIORITY)
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].title == "Python lernen"
    assert sorted_tasks[1].title == "Git lernen"
    assert sorted_tasks[2].title == "Einkaufen"
    assert sorted_tasks[0].priority == Priority.HIGH
    assert sorted_tasks[1].priority == Priority.MEDIUM
    assert sorted_tasks[2].priority == Priority.LOW


def test_sort_tasks_by_due_date_returns_earliest_due_date_first_and_none_last() -> None:
    repository = FakeTaskRepository()
    repository.add(Task("Später", due_date=date(2026, 10, 20)))
    repository.add(Task("Ohne Datum"))
    repository.add(Task("Früher", due_date=date(2026, 9, 10)))
    tasks = repository.get_all()
    sorted_tasks_use_case = SortTasks()
    sorted_tasks = sorted_tasks_use_case.execute(tasks, SortField.DUE_DATE)
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].title == "Früher"
    assert sorted_tasks[1].title == "Später"
    assert sorted_tasks[2].title == "Ohne Datum"


def test_sort_tasks_by_title_with_reverse_returns_tasks_in_reverse_alphabetical_order() -> (
    None
):
    repository = FakeTaskRepository()
    repository.add(Task("Einkaufen"))
    repository.add(Task("Git lernen"))
    repository.add(Task("Python lernen"))
    tasks = repository.get_all()
    sorted_task_use_case = SortTasks()
    sorted_tasks = sorted_task_use_case.execute(tasks, SortField.TITLE, reverse=True)
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].title == "Python lernen"
    assert sorted_tasks[1].title == "Git lernen"
    assert sorted_tasks[2].title == "Einkaufen"


def test_sort_tasks_does_not_change_repository_order() -> None:
    repository = FakeTaskRepository()
    repository.add(Task("Python lernen"))
    repository.add(Task("Einkaufen"))
    repository.add(Task("Git lernen"))
    tasks = repository.get_all()
    sorted_task_use_case = SortTasks()
    sorted_task_use_case.execute(tasks, SortField.TITLE)
    original_task_list = repository.get_all()
    assert len(original_task_list) == 3
    assert original_task_list[0].title == "Python lernen"
    assert original_task_list[1].title == "Einkaufen"
    assert original_task_list[2].title == "Git lernen"


def test_sort_tasks_with_empty_repository_returns_empty_list() -> None:
    repository = FakeTaskRepository()
    tasks = repository.get_all()
    sorted_task_use_case = SortTasks()
    sorted_tasks = sorted_task_use_case.execute(tasks, SortField.TITLE)
    assert len(sorted_tasks) == 0
    assert sorted_tasks == []
