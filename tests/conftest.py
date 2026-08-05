import pytest
from taskflow.task_service import TaskService

@pytest.fixture
def service() -> TaskService:
    return TaskService()

@pytest.fixture
def service_with_tasks() -> TaskService:
    service = TaskService()
    service.add_task("Python lernen")
    service.add_task("Git lernen")
    return service