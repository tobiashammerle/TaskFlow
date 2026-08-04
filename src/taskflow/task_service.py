from taskflow.task import Task

class TaskService:
    """Verwaltet die Aufgaben der Anwendung."""
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, title: str) -> bool:
        """Fügt eine Aufgabe hinzu, wenn der Titel nicht leer ist."""

        try:
            task = Task(title)
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
        return self.tasks
    