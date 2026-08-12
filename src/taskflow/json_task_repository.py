import json
import logging
from pathlib import Path

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

    # def load(self) -> list[Task]:
    #     """Lädt Aufgaben aus der JSON-Datei."""
    #     if not self.file_path.exists():
    #         logger.warning("Datei %s existiert nicht. Start mit leerer Aufgabenliste.", self.file_path)
    #         return []
    #     with self.file_path.open("r", encoding="utf-8") as file:
    #         data = json.load(file)
    #         tasks: list[Task] = []
    #         tasks = [Task.from_dict(item) for item in data]
    #         logger.info("%d Aufgaben geladen", len(tasks))
    #         return tasks

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
