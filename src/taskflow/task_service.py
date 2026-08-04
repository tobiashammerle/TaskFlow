class TaskService:
    """Verwaltet die Aufgaben der Anwendung."""
    def __init__(self) -> None:
        self.tasks: list[str] = []

    def add_task(self, title: str) -> bool:
        """Fügt eine Aufgabe hinzu, wenn der Titel nicht leer ist."""
        cleaned_title = title.strip()
        if not cleaned_title:
            return False
        self.tasks.append(cleaned_title)
        return True

    def remove_task(self, index: int) -> str | None:
        """Entfernt eine Aufgabe anhand ihres Index. """
        if index < 0 or index >= len(self.tasks):
            return None
        return self.tasks.pop(index)

    def get_tasks(self) -> list[str]:
        """Gibt die aktuelle Aufgabenliste zurück."""
        return self.tasks
    