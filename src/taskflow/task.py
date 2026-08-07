from taskflow.priority import Priority
from datetime import date
from taskflow.exceptions import EmptyTitleError



class Task:
    """Repräsentiert eine einzelne Aufgabe"""
    def __init__(self, title: str, priority: Priority = Priority.MEDIUM, due_date: date | None = None) -> None:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise EmptyTitleError("Der Titel darf nicht leer sein. ")
        self.title = cleaned_title
        self.completed = False
        self.priority = priority
        self.due_date = due_date

    def complete(self) -> None:
        """Markiert die Aufgabe als erledigt."""
        self.completed = True

    def __str__(self) -> str:
        """Gibt eine lesbare Darstellung der Aufgabe zurück."""
        status = "\u2713" if self.completed else " "
        result = (f"[{status}] {self.title} - {self.priority.value}")
        if self.due_date is not None:
            result += f" - fällig: {self.due_date.isoformat()}"
        return result

    def __repr__(self) -> str:
        """Gibt eine eindeutige Entwicklerdarstellung zurück."""
        return (
            "Task("
            f"title={self.title!r},"
            f"completed={self.completed!r},"
            f"priority={self.priority!r},"
            f"due_date={self.due_date!r}"
            ")"
        )
    def to_dict(self) -> dict[str, object]:
        """Wandelt die Aufgabe in ein Dictionary um."""
        return {
            "title": self.title,
            "completed": self.completed,
            "priority": self.priority.value,
            "due_date": (self.due_date.isoformat() if self.due_date is not None else None),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Task":
        """Erstellt eine Aufgabe aus einem Dictionary."""
        priority = Priority(str(data.get("priority", Priority.MEDIUM.value)))
        due_date_value = data.get("due_date")
        due_date = (date.fromisoformat(str(due_date_value)) if due_date_value is not None else None)
        task = cls(
            str(data["title"]),
            priority=priority,
            due_date=due_date,
        )
        if bool(data.get("completed", False)):
            task.complete()
        return task
    