from taskflow.filter_type import FilterType
from taskflow.task import Task
from taskflow.task_repository import TaskRepository


class FilterTasks:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, filter_type: FilterType) -> list[Task]:
        tasks = self.repository.get_all()
        if filter_type == FilterType.COMPLETED:
            return [task for task in tasks if task.completed]
        elif filter_type == FilterType.OPEN:
            return [task for task in tasks if not task.completed]
        elif filter_type == FilterType.ALL:
            return tasks
