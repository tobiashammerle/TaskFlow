from taskflow.priority import Priority
from taskflow.sort_field import SortField
from taskflow.task import Task


class SortTasks:
    def execute(
        self, tasks: list[Task], field: SortField, reverse: bool = False
    ) -> list[Task]:
        if field == SortField.TITLE:
            return sorted(tasks, key=lambda task: task.title, reverse=reverse)
        elif field == SortField.PRIORITY:
            priority_order = {
                Priority.HIGH: 1,
                Priority.MEDIUM: 2,
                Priority.LOW: 3,
            }
            return sorted(
                tasks, key=lambda task: priority_order[task.priority], reverse=reverse
            )
        elif field == SortField.DUE_DATE:
            return sorted(
                tasks,
                key=lambda task: (task.due_date is None, task.due_date),
                reverse=reverse,
            )
        raise ValueError(f"Ungültiges Sortierfeld: {field}")
