class Task:
    """Repräsentiert eine einzelne Aufgabe"""
    def __init__(self, title: str) -> None:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("Der Titel darf nicht leer sein. ")
        self.title = cleaned_title
        self.completed = False
        