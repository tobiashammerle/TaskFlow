from taskflow.application.complete_task import CompleteTask
from taskflow.application.filter_tasks import FilterTasks
from taskflow.filter_type import FilterType
from taskflow.task import Task
from tests.fakes import FakeTaskRepository


def test_filter_tasks_with_filter_type_completed_returns_all_completed_tasks() -> None:
    repository = FakeTaskRepository()
    complete_task = CompleteTask(repository)
    Task_A = Task("Task A")
    Task_B = Task("Task B")
    Task_C = Task("Task C")
    repository.add(Task_A)
    repository.add(Task_B)
    repository.add(Task_C)
    complete_task.execute(Task_A.id)
    complete_task.execute(Task_C.id)
    tasks = repository.get_all()
    filter_tasks = FilterTasks()
    filtered_tasks = filter_tasks.execute(tasks, FilterType.COMPLETED)
    assert len(filtered_tasks) == 2
    assert filtered_tasks[0].title == "Task A"
    assert filtered_tasks[1].title == "Task C"


def test_filter_tasks_with_filter_type_open_returns_all_open_tasks() -> None:
    repository = FakeTaskRepository()
    complete_task = CompleteTask(repository)
    Task_A = Task("Task A")
    Task_B = Task("Task B")
    Task_C = Task("Task C")
    repository.add(Task_A)
    repository.add(Task_B)
    repository.add(Task_C)
    complete_task.execute(Task_A.id)
    complete_task.execute(Task_C.id)
    tasks = repository.get_all()
    filter_tasks = FilterTasks()
    filtered_tasks = filter_tasks.execute(tasks, FilterType.OPEN)
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].title == "Task B"


def test_filter_tasks_with_filter_type_all_returns_all_tasks() -> None:
    repository = FakeTaskRepository()
    complete_task = CompleteTask(repository)
    Task_A = Task("Task A")
    Task_B = Task("Task B")
    Task_C = Task("Task C")
    repository.add(Task_A)
    repository.add(Task_B)
    repository.add(Task_C)
    complete_task.execute(Task_A.id)
    complete_task.execute(Task_C.id)
    tasks = repository.get_all()
    filter_tasks = FilterTasks()
    filtered_tasks = filter_tasks.execute(tasks, FilterType.ALL)
    assert len(filtered_tasks) == 3
    assert filtered_tasks[0].title == "Task A"
    assert filtered_tasks[1].title == "Task B"
    assert filtered_tasks[2].title == "Task C"


def test_filter_tasks_with_empty_repository_returns_empty_list() -> None:
    repository = FakeTaskRepository()
    tasks = repository.get_all()
    filter_tasks = FilterTasks()
    filtered_tasks = filter_tasks.execute(tasks, FilterType.ALL)
    assert len(filtered_tasks) == 0
    assert filtered_tasks == []


def test_filter_tasks_does_not_change_original_task_list() -> None:
    repository = FakeTaskRepository()
    complete_task = CompleteTask(repository)
    Task_A = Task("Task A")
    Task_B = Task("Task B")
    Task_C = Task("Task C")
    repository.add(Task_A)
    repository.add(Task_B)
    repository.add(Task_C)
    complete_task.execute(Task_B.id)
    tasks = repository.get_all()
    filter_tasks = FilterTasks()
    filtered_tasks = filter_tasks.execute(tasks, FilterType.COMPLETED)
    assert len(tasks) == 3
    assert tasks[0].title == "Task A"
    assert tasks[1].title == "Task B"
    assert tasks[2].title == "Task C"
    assert filtered_tasks[0].title == "Task B"
    assert len(filtered_tasks) == 1
