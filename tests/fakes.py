from uuid import UUID

from taskflow.task import Task


class FakeTaskRepository:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def save(self, tasks: list[Task]) -> None:
        self.tasks = tasks.copy()

    def get_all(self) -> list[Task]:
        return self.tasks.copy()

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def delete(self, task_id: UUID) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def update(self, task: Task) -> None:
        for i, existing_task in enumerate(self.tasks):
            if existing_task.id == task.id:
                self.tasks[i] = task
                break

    def get_by_id(self, task_id: UUID) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
