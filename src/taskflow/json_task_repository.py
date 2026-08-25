import json
import logging
from pathlib import Path
from uuid import UUID

from taskflow.task import Task

logger = logging.getLogger(__name__)


class JsonTaskRepository:
    """Speichert und lädt Aufgaben in JSON-Datei."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def save(self, tasks: list[Task]) -> None:
        """Speichert alle Aufgaben als JSON."""

        data = [task.to_dict() for task in tasks]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            logger.info("%d Aufgaben gespeichert", len(tasks))

    def get_all(self) -> list[Task]:
        """Lädt Aufgaben aus der JSON-Datei."""
        if not self.file_path.exists():
            logger.warning(
                "Datei %s existiert nicht. Start mit leerer Aufgabenliste.",
                self.file_path,
            )
            return []
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            tasks = [Task.from_dict(item) for item in data]
            logger.info("%d Aufgaben geladen", len(tasks))
            return tasks

    def get_by_id(self, task_id: UUID) -> Task | None:
        """Lädt eine Aufgabe anhand ihrer ID aus der JSON-Datei."""
        tasks = self.get_all()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def add(self, task: Task) -> None:
        """Fügt eine Aufgabe hinzu und speichert sie in der JSON-Datei."""
        tasks = self.get_all()
        tasks.append(task)
        self.save(tasks)

    def update(self, task: Task) -> None:
        """Aktualisiert eine Aufgabe in der JSON-Datei."""
        tasks = self.get_all()
        for i, existing_task in enumerate(tasks):
            if existing_task.id == task.id:
                tasks[i] = task
                self.save(tasks)
                return
        raise ValueError(f"Keine Aufgabe mit ID {task.id} gefunden.")

    def delete(self, task_id: UUID) -> None:
        """Löscht eine Aufgabe anhand ihrer ID aus der JSON-Datei."""
        tasks = self.get_all()
        tasks = [task for task in tasks if task.id != task_id]
        self.save(tasks)
