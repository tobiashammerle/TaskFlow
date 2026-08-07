import pytest
from taskflow.task_service import TaskService
from taskflow.task import Task


class FakeTaskRepository:
    def __init__(self) -> None:
        self.tasks: list[Task]=[]
    def load(self) -> list[Task]:
        return self.tasks.copy()
    def save(self, tasks: list[Task]) -> None:
        self.tasks = tasks.copy()

@pytest.fixture
def service() -> TaskService:
    repository = FakeTaskRepository()
    return TaskService(repository)

@pytest.fixture
def service_with_tasks() -> TaskService:
    repository = FakeTaskRepository()
    service = TaskService(repository)
    service.add_task("Python lernen")
    service.add_task("Git lernen")
    return service

@pytest.fixture
def repository_with_tasks() -> FakeTaskRepository:
    repository = FakeTaskRepository()
    repository.tasks = [Task("Python lernen"), Task("Git lernen")]
    return repository