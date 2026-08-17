import logging
from datetime import date
from uuid import UUID

from taskflow.exceptions import TaskNotFoundError
from taskflow.filter_type import FilterType
from taskflow.priority import Priority
from taskflow.sort_field import SortField
from taskflow.task import Task
from taskflow.task_repository import TaskRepository
from taskflow.task_statistics import TaskStatistics

logger = logging.getLogger(__name__)


class TaskService:
    """Verwaltet die Aufgaben der Anwendung."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def add_task(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> None:
        """Fügt eine Aufgabe hinzu, wenn der Titel nicht leer ist."""

        task = Task(title, priority=priority, due_date=due_date)
        self.repository.add(task)
        logger.info("Aufgabe erstellt: %s", task.title)

    def remove_task(self, task_id: UUID) -> Task:
        """Entfernt eine Aufgabe anhand ihrer ID."""
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Keine Aufgabe mit ID {task_id} gefunden.")
        self.repository.delete(task_id)
        logger.info("Aufgabe gelöscht: %s", task.title)
        return task

    def get_tasks(self) -> list[Task]:
        """Gibt die aktuelle Aufgabenliste zurück."""
        return self.repository.get_all()

    def complete_task(self, task_id: UUID) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Keine Aufgabe mit ID {task_id} gefunden.")
        task.complete()
        self.repository.update(task)
        logger.info("Aufgabe abgeschlossen: %s", task.title)
        return task

    def sort_tasks(self, field: SortField, reverse: bool = False) -> None:
        tasks = (
            self.repository.get_all()
        )  # Aktualisiere die Aufgabenliste vor dem Sortieren
        if field == SortField.TITLE:
            tasks.sort(key=lambda task: task.title, reverse=reverse)
        elif field == SortField.PRIORITY:
            priority_order = {
                Priority.HIGH: 1,
                Priority.MEDIUM: 2,
                Priority.LOW: 3,
            }
            tasks.sort(
                key=lambda task: priority_order[task.priority],
                reverse=reverse,
            )
        elif field == SortField.DUE_DATE:
            tasks.sort(
                key=lambda task: (task.due_date is None, task.due_date), reverse=reverse
            )
        self.repository.save(tasks)  # Speichere die sortierte Liste in der Repository

    def filter_tasks(self, filter_type: FilterType) -> list[Task]:
        tasks = (
            self.repository.get_all()
        )  # Aktualisiere die Aufgabenliste vor dem Filtern
        if filter_type == FilterType.COMPLETED:
            return [task for task in tasks if task.completed]
        elif filter_type == FilterType.OPEN:
            return [task for task in tasks if not task.completed]
        elif filter_type == FilterType.HIGH_PRIORITY:
            return [task for task in tasks if task.priority == Priority.HIGH]
        elif filter_type == FilterType.MEDIUM_PRIORITY:
            return [task for task in tasks if task.priority == Priority.MEDIUM]
        elif filter_type == FilterType.LOW_PRIORITY:
            return [task for task in tasks if task.priority == Priority.LOW]
        elif filter_type == FilterType.WITH_DUE_DATE:
            return [task for task in tasks if task.due_date is not None]
        elif filter_type == FilterType.WITHOUT_DUE_DATE:
            return [task for task in tasks if task.due_date is None]
        return tasks

    def search_tasks(self, search_text: str) -> list[Task]:
        normalized_search_text = search_text.strip().casefold()
        tasks = (
            self.repository.get_all()
        )  # Aktualisiere die Aufgabenliste vor der Suche
        return [
            task for task in tasks if normalized_search_text in task.title.casefold()
        ]

    def get_statistics(self) -> None:
        tasks = (
            self.repository.get_all()
        )  # Aktualisiere die Aufgabenliste vor der Berechnung der Statistiken
        return TaskStatistics(
            total_tasks=len(tasks),
            completed_tasks=sum(task.completed for task in tasks),
            open_tasks=sum(not task.completed for task in tasks),
            high_priority_tasks=sum(task.priority == Priority.HIGH for task in tasks),
        )
