from taskflow.filter_type import FilterType
from taskflow.priority import Priority
from taskflow.task import Task


class FilterTasks:
    def execute(self, tasks: list[Task], filter_type: FilterType) -> list[Task]:
        if filter_type == FilterType.COMPLETED:
            return [task for task in tasks if task.completed]
        elif filter_type == FilterType.OPEN:
            return [task for task in tasks if not task.completed]
        elif filter_type == FilterType.ALL:
            return tasks
        elif filter_type == FilterType.HIGH_PRIORITY:
            return [task for task in tasks if task.priority == Priority.HIGH]
        elif filter_type == FilterType.LOW_PRIORITY:
            return [task for task in tasks if task.priority == Priority.LOW]
        elif filter_type == FilterType.MEDIUM_PRIORITY:
            return [task for task in tasks if task.priority == Priority.MEDIUM]
        elif filter_type == FilterType.WITH_DUE_DATE:
            return [task for task in tasks if task.due_date is not None]
        elif filter_type == FilterType.WITHOUT_DUE_DATE:
            return [task for task in tasks if task.due_date is None]
