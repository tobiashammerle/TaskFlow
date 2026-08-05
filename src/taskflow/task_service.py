from datetime import date
from taskflow.priority import Priority
from taskflow.task import Task

class TaskService:
    """Verwaltet die Aufgaben der Anwendung."""
    def __init__(self, tasks: list[Task] | None = None) -> None:
        self.tasks = tasks if tasks is not None else []

    def add_task(self, title: str, priority: Priority = Priority.MEDIUM, due_date: date | None = None) -> bool:
        """Fügt eine Aufgabe hinzu, wenn der Titel nicht leer ist."""

        try:
            task = Task(title, priority=priority, due_date=due_date)
        except ValueError:
            return False
        self.tasks.append(task)
        return True
   

    def remove_task(self, index: int) -> Task | None:
        """Entfernt eine Aufgabe anhand ihres Index. """
        if index < 0 or index >= len(self.tasks):
            return None
        return self.tasks.pop(index)

    def get_tasks(self) -> list[Task]:
        """Gibt die aktuelle Aufgabenliste zurück."""
        return self.tasks.copy()

    def complete_task(self, index: int) -> Task | None:
        if index < 0 or index >= len(self.tasks):
            return None
        task = self.tasks[index]
        task.complete()
        return task
    