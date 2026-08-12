from datetime import date

import pytest

from taskflow.exceptions import EmptyTitleError
from taskflow.priority import Priority
from taskflow.task import Task


def test_complete_marks_task_as_completed() -> None:
    task = Task("Python lernen")
    task.complete()
    assert task.completed is True


def test_str_returns_open_task() -> None:
    task = Task("Python lernen")
    assert str(task) == "[ ] Python lernen - MEDIUM"


def test_str_returns_completed_task() -> None:
    task = Task("Python lernen")
    task.complete()
    assert str(task) == "[\u2713] Python lernen - MEDIUM"


def test_str_includes_custom_priority() -> None:
    task = Task("Python lernen", priority=Priority.HIGH)
    assert str(task) == "[ ] Python lernen - HIGH"


def test_task_stores_cleaned_title() -> None:
    task = Task("   Python lernen   ")
    assert task.title == "Python lernen"


def test_empty_title_raises_empty_title_error() -> None:
    with pytest.raises(EmptyTitleError):
        Task("    ")


def test_task_has_medium_priority_by_default() -> None:
    task = Task("Python lernen")
    assert task.priority == Priority.MEDIUM


def test_task_has_no_due_date_by_default() -> None:
    task = Task("Python lernen")
    assert task.due_date is None


def test_task_accepts_due_date() -> None:
    due_date = date(2026, 8, 31)
    task = Task("Steuererklärung", due_date=due_date)
    assert task.due_date == due_date


def test_str_returns_task_without_due_date() -> None:
    task = Task("Python lernen")
    assert str(task) == "[ ] Python lernen - MEDIUM"


def test_str_includes_due_date() -> None:
    task = Task("Steuererklärung", priority=Priority.HIGH, due_date=date(2026, 8, 31))
    assert str(task) == "[ ] Steuererklärung - HIGH - fällig: 2026-08-31"


def test_repr_returns_developer_representation() -> None:
    task = Task("Python lernen", priority=Priority.HIGH, due_date=date(2026, 8, 31))
    assert repr(task) == (
        "Task("
        "title='Python lernen',"
        "completed=False,"
        "priority=<Priority.HIGH: 'HIGH'>,"
        "due_date=datetime.date(2026, 8, 31)"
        ")"
    )


def test_to_dict_returns_expected_dictionary() -> None:
    task = Task("Python lernen", priority=Priority.HIGH, due_date=date(2026, 8, 31))
    assert task.to_dict() == {
        "title": "Python lernen",
        "completed": False,
        "priority": "HIGH",
        "due_date": "2026-08-31",
    }


def test_from_dict_creates_task() -> None:
    data = {
        "title": "Python lernen",
        "completed": True,
        "priority": "HIGH",
        "due_date": "2026-08-31",
    }
    task = Task.from_dict(data)
    assert task.title == "Python lernen"
    assert task.completed is True
    assert task.priority == Priority.HIGH
    assert task.due_date == date(2026, 8, 31)
