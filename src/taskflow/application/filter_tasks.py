from taskflow.filter_type import FilterType
from taskflow.task import Task


class FilterTasks:
    def execute(self, tasks: list[Task], filter_type: FilterType) -> list[Task]:
        if filter_type == FilterType.COMPLETED:
            return [task for task in tasks if task.completed]
        elif filter_type == FilterType.OPEN:
            return [task for task in tasks if not task.completed]
        elif filter_type == FilterType.ALL:
            return tasks
