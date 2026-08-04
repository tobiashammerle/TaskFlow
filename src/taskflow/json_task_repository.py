import json
from pathlib import Path
from taskflow.task import Task

class JsonTaskRepository:
    """Speichert und lädt Aufgaben in JSON-Datei."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def save(self, tasks: list[Task]) -> None:
        """Speichert alle Aufgaben als JSON."""
        data = [
            {
                "title": task.title,
                "completed": task.completed,
            }
            for task in tasks
        ]
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


    def load(self) -> list[Task]:
        """Lädt Aufgaben aus der JSON-Datei."""
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            tasks: list[Task] = []
            for item in data:
                task = Task(item["title"])
                if item["completed"]:
                    task.complete()
                tasks.append(task)
            return tasks


    