from dataclasses import dataclass

@dataclass
class TaskStatistics:
    total_tasks: int
    completed_tasks: int
    open_tasks: int
    high_priority_tasks: int
    