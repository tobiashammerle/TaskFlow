import pytest
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

def test_remove_task_removes_existing_task(service_with_tasks: TaskService) -> None:
    removed_task = service_with_tasks.remove_task(0)
    tasks = service_with_tasks.get_tasks()
    assert removed_task is not None
    assert removed_task.title == "Python lernen"
    assert len(tasks) == 1
    assert tasks[0].title == "Git lernen"

def test_remove_task_returns_none_for_negative_index() -> None:
    service = TaskService()
    service.add_task("Python lernen")
    removed_task = service.remove_task(-1)
    assert removed_task is None
    assert len(service.get_tasks()) == 1

def test_remove_task_returns_none_for_index_that_is_too_large() -> None:
    service = TaskService()
    service.add_task("Python lernen")
    removed_task = service.remove_task(1)
    assert removed_task is None
    assert len(service.get_tasks()) == 1

def test_complete_task_marks_task_as_completed() -> None:
    service = TaskService()
    service.add_task("Python lernen")
    completed_task = service.complete_task(0)
    tasks = service.get_tasks()
    assert completed_task is not None
    assert completed_task.completed is True
    assert tasks[0].completed is True

def test_complete_task_returns_none_for_negative_index() -> None:
    service = TaskService()
    service.add_task("Python lernen")
    completed_task = service.complete_task(-1)
    assert completed_task is None
    assert service.get_tasks()[0].completed is False

def test_complete_task_returns_none_for_index_that_is_too_large() -> None:
    service = TaskService()
    service.add_task("Python lernen")
    completed_task = service.complete_task(1)
    assert completed_task is None
    assert service.get_tasks()[0].completed is False

def test_constructor_uses_existing_tasks() -> None:
    tasks = [Task("Python lernen"), Task("Git lernen")]
    service = TaskService(tasks)
    assert service.get_tasks() == tasks

def test_constructor_creates_empty_task_list() -> None:
    service = TaskService()
    assert service.get_tasks() == []

