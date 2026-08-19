from taskflow.task import Task
from taskflow.task_repository import TaskRepository


class GetTasks:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Task]:
        return self.repository.get_all()
