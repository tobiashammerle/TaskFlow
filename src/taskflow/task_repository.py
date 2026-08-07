from typing import Protocol
from taskflow.task import Task

class TaskRepository(Protocol):
    """ Schnittstelle für Task-Repositories."""

    def load(self) -> list[Task]:
        ... #"Ellipsis-Objekt" besteht aus diesen 3 Punkten - und steht für "hier gibt es bewusst keine Implementierung"

    def save(self, tasks: list[Task]) -> None:
        ...
