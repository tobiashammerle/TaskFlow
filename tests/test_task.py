from taskflow.priority import Priority
import pytest
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
    task = Task("Python lernen", priority = Priority.HIGH)
    assert str(task) == "[ ] Python lernen - HIGH"

def test_task_stores_cleaned_title() -> None:
    task = Task("   Python lernen   ")
    assert task.title == "Python lernen"

def test_empty_title_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Task("    ")

def test_task_has_medium_priority_by_default() -> None:
    task = Task("Python lernen")
    assert task.priority == Priority.MEDIUM
