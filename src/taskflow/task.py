class Task:
    """Repräsentiert eine einzelne Aufgabe"""
    def __init__(self, title: str) -> None:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("Der Titel darf nicht leer sein. ")
        self.title = cleaned_title
        self.completed = False

    def complete(self) -> None:
        """Markiert die Aufgabe als erledigt."""
        self.completed = True

    def __str__(self) -> str:
        """Gibt eine lesbare Darstellung der Aufgabe zurück."""
        status = "\u2713" if self.completed else " "
        return f"[{status}] {self.title}"
