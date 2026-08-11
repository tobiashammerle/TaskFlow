from taskflow.task import Task

class FakeTaskRepository:
    def __init__(self) -> None:
        self.tasks: list[Task]=[]
    def save(self, tasks: list[Task]) -> None:
        self.tasks = tasks.copy()
    def get_all(self) -> list[Task]:
        return self.tasks.copy()