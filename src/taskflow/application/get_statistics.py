from taskflow.priority import Priority
from taskflow.task import Task
from taskflow.task_statistics import TaskStatistics


class GetStatistics:
    def execute(self, tasks: list[Task]) -> TaskStatistics:
        return TaskStatistics(
            total_tasks=len(tasks),
            completed_tasks=sum(task.completed for task in tasks),
            open_tasks=sum(not task.completed for task in tasks),
            high_priority_tasks=sum(task.priority == Priority.HIGH for task in tasks),
        )
