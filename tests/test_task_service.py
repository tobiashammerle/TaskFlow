import pytest
from datetime import date
from taskflow.task_statistics import TaskStatistics
from taskflow.filter_type import FilterType
from taskflow.sort_field import SortField
from taskflow.priority import Priority
from taskflow.task import Task
from taskflow.task_service import TaskService


def test_add_task_adds_new_task(service: TaskService) -> None:
    service.add_task("Python lernen")
    tasks = service.get_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Python lernen"
    assert tasks[0].completed is False

@pytest.mark.parametrize(
        "title",
        [
            "",
            "   ",
            "\t",
            "\n",
        ]
)
def test_add_task_returns_false_for_invalid_title(service: TaskService, title: str) -> None:
    result = service.add_task(title)
    assert result is False
    assert service.get_tasks() == []

def test_add_task_returns_true_for_valid_title(service: TaskService) -> None:
    result = service.add_task("Python lernen")
    assert result is True

# def test_add_task_returns_false_for_empty_title(service: TaskService) -> None:
#     result = service.add_task("")
#     assert result is False
#     assert service.get_tasks() == []

# def test_add_task_returns_false_for_whitespace_title(service: TaskService) -> None:
#     result = service.add_task("     ")
#     assert result is False
#     assert service.get_tasks() == []

def test_add_task_strips_title(service: TaskService) -> None:
    service.add_task("   Python lernen  ")
    tasks = service.get_tasks()
    assert tasks[0].title == "Python lernen"

def test_add_task_with_priority(service: TaskService) -> None:
    service.add_task("Python lernen", priority = Priority.HIGH)
    task = service.get_tasks()[0]
    assert task.priority == Priority.HIGH

def test_remove_task_removes_existing_task(service_with_tasks: TaskService) -> None:
    removed_task = service_with_tasks.remove_task(0)
    tasks = service_with_tasks.get_tasks()
    assert removed_task is not None
    assert removed_task.title == "Python lernen"
    assert len(tasks) == 1
    assert tasks[0].title == "Git lernen"

def test_remove_task_returns_none_for_negative_index(service: TaskService) -> None:
    service.add_task("Python lernen")
    removed_task = service.remove_task(-1)
    assert removed_task is None
    assert len(service.get_tasks()) == 1

def test_remove_task_returns_none_for_index_that_is_too_large(service: TaskService) -> None:
    service.add_task("Python lernen")
    removed_task = service.remove_task(1)
    assert removed_task is None
    assert len(service.get_tasks()) == 1

def test_complete_task_marks_task_as_completed(service: TaskService) -> None:
    service.add_task("Python lernen")
    completed_task = service.complete_task(0)
    tasks = service.get_tasks()
    assert completed_task is not None
    assert completed_task.completed is True
    assert tasks[0].completed is True

def test_complete_task_returns_none_for_negative_index(service: TaskService) -> None:
    service.add_task("Python lernen")
    completed_task = service.complete_task(-1)
    assert completed_task is None
    assert service.get_tasks()[0].completed is False

def test_complete_task_returns_none_for_index_that_is_too_large(service: TaskService) -> None:
    service.add_task("Python lernen")
    completed_task = service.complete_task(1)
    assert completed_task is None
    assert service.get_tasks()[0].completed is False

def test_constructor_loads_tasks_from_repository(repository_with_tasks) -> None:
    service = TaskService(repository_with_tasks)
    tasks = service.get_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Python lernen"
    assert tasks[1].title == "Git lernen"

def test_constructor_creates_empty_task_list(service: TaskService) -> None:
    assert service.get_tasks() == []

def test_add_task_with_due_date(service: TaskService) -> None:
    due_date = date(2026, 8, 31)
    service.add_task("Steuererklärung", due_date=due_date)
    task = service.get_tasks()[0]
    assert task.due_date == due_date

def test_get_tasks_returns_copy(service: TaskService) -> None:
    service.add_task("Python lernen")
    tasks = service.get_tasks()
    tasks.clear()
    assert len(service.get_tasks())==1

def test_sort_tasks_by_title(service: TaskService) -> None:
    service.add_task("C")
    service.add_task("A")
    service.add_task("B")
    service.sort_tasks(SortField.TITLE)
    titles = [task.title for task in service.get_tasks()]
    assert titles == [
        "A",
        "B",
        "C",
    ]

def test_sort_task_by_priority(service: TaskService) -> None:
    service.add_task("Mittlere Aufgabe", priority=Priority.MEDIUM)
    service.add_task("Niedrige Aufgabe", priority=Priority.LOW)
    service.add_task("Hohe Aufgabe", priority=Priority.HIGH)

    service.sort_tasks(SortField.PRIORITY)
    priorities = [
        task.priority for task in service.get_tasks()
    ]

    assert priorities == [
        Priority.HIGH,
        Priority.MEDIUM,
        Priority.LOW,
    ]

def test_sort_tasks_by_due_date(service: TaskService) -> None:
    service.add_task("Python lernen", due_date=date(2026, 8, 20))
    service.add_task("Steuererklärung", due_date=date(2026, 8, 15))
    service.add_task("Git üben", due_date=date(2026, 8, 10))

    service.sort_tasks(SortField.DUE_DATE)
    titles = [task.title for task in service.get_tasks()]
    assert titles == [
        "Git üben",
        "Steuererklärung",
        "Python lernen",
    ]

def test_sort_tasks_by_due_date_without_due_date(service: TaskService) -> None:
    service.add_task("Python lernen")
    service.add_task("Steuererklärung", due_date=date(2026, 8, 15))
    service.add_task("Git üben", due_date=date(2026, 8, 10))
    service.sort_tasks(SortField.DUE_DATE)
    titles = [
        task.title for task in service.get_tasks()
    ]

    assert titles == [
        "Git üben",
        "Steuererklärung",
        "Python lernen",
    ]

def test_filter_completed_tasks(service: TaskService) -> None:
    service.add_task("Python lernen")
    service.add_task("Git üben")
    service.get_tasks()[1].complete()
    completed = service.filter_tasks(FilterType.COMPLETED)
    assert len(completed) == 1
    assert completed[0].title == "Git üben"

def test_filter_open_tasks(service: TaskService) -> None:
    service.add_task("Python lernen")
    service.add_task("Git üben")
    service.complete_task(1)
    open_tasks = service.filter_tasks(FilterType.OPEN)
    assert len(open_tasks) == 1
    assert open_tasks[0].title == "Python lernen"
    assert open_tasks[0].completed is False

def test_filter_all_tasks(service: TaskService) -> None:
    service.add_task("Python lernen")
    service.add_task("Git üben")
    service.complete_task(1)
    all_tasks = service.filter_tasks(FilterType.ALL)
    assert len(all_tasks) == 2

def test_filter_high_priority_tasks(service: TaskService) -> None:
    service.add_task("Python lernen", priority=Priority.HIGH)
    service.add_task("Git üben", priority=Priority.LOW)
    high_tasks = service.filter_tasks(FilterType.HIGH_PRIORITY)
    assert len(high_tasks) == 1
    assert high_tasks[0].title == "Python lernen"
    assert high_tasks[0].priority == Priority.HIGH

@pytest.mark.parametrize(
    ("filter_type", "priority", "expected_title"),
    [
        (
            FilterType.HIGH_PRIORITY,
            Priority.HIGH,
            "Hohe Aufgabe",
        ),
        (
            FilterType.MEDIUM_PRIORITY,
            Priority.MEDIUM,
            "Mittlere Aufgabe",
        ),
        (
            FilterType.LOW_PRIORITY,
            Priority.LOW,
            "Niedrige Aufgabe"
        ),
    ]
)
def test_filter_tasks_by_priority(service: TaskService,
                                  filter_type: FilterType,
                                  priority: Priority,
                                  expected_title: str) -> None:
    service.add_task(
        "Hohe Aufgabe",
        priority=Priority.HIGH,
    )
    service.add_task(
        "Mittlere Aufgabe",
        priority=Priority.MEDIUM,
    )
    service.add_task(
        "Niedrige Aufgabe",
        priority=Priority.LOW,
    )
    filtered_tasks = service.filter_tasks(filter_type)
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].title == expected_title
    assert filtered_tasks[0].priority == priority

def test_filter_tasks_with_due_date(service: TaskService) -> None:
    service.add_task("Steuererklärung", due_date=date(2026, 8, 31))
    service.add_task("Python lernen")
    filtered_tasks = service.filter_tasks(FilterType.WITH_DUE_DATE)
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].title == "Steuererklärung"
    assert filtered_tasks[0].due_date == date(2026, 8, 31)

def test_filter_tasks_without_due_date(service: TaskService) -> None:
    service.add_task("Steuererklärung", due_date=date(2026, 8, 31))
    service.add_task("Python lernen")
    filtered_tasks = service.filter_tasks(FilterType.WITHOUT_DUE_DATE)
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].title == "Python lernen"
    assert filtered_tasks[0].due_date is None

def test_search_tasks_by_title(service: TaskService) -> None:
    service.add_task("Python lernen")
    service.add_task("Git lernen")
    service.add_task("Python testen")
    results = service.search_tasks("python")
    assert len(results) == 2
    assert results[0].title == "Python lernen"
    assert results[1].title == "Python testen"

def test_search_tasks_is_case_insensitive(service: TaskService) -> None:
    service.add_task("Python lernen")
    results = service.search_tasks("PYTHON")
    assert len(results) == 1
    assert results[0].title == "Python lernen"

def test_search_tasks_with_empty_text_returns_all_tasks(service: TaskService) -> None:
    service.add_task("Python lernen")
    service.add_task("Git lernen")
    results = service.search_tasks("")
    assert len(results) == 2

def test_search_tasks_returns_empty_list_when_nothing_matches(service: TaskService) -> None:
    service.add_task("Python lernen")
    results = service.search_tasks("Docker")
    assert results == []

def test_get_statistics_for_empty_service(service: TaskService) -> None:
    statistics = service.get_statistics()
    assert statistics == TaskStatistics(
        total_tasks=0,
        completed_tasks=0,
        open_tasks=0,
        high_priority_tasks=0,
    )

def test_get_statistics(service: TaskService) -> None:
    service.add_task("Python lernen", priority=Priority.HIGH)
    service.add_task("Git üben", priority=Priority.MEDIUM)
    service.add_task("Docker lernen", priority=Priority.HIGH)
    service.complete_task(1)
    statistics = service.get_statistics()
    assert statistics == TaskStatistics(
        total_tasks=3,
        completed_tasks=1,
        open_tasks=2,
        high_priority_tasks=2,
    )
