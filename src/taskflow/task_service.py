import logging
from datetime import date
from uuid import UUID

from taskflow.application.create_task import CreateTask
from taskflow.application.filter_tasks import FilterTasks
from taskflow.application.get_statistics import GetStatistics
from taskflow.application.remove_task import RemoveTask
from taskflow.application.search_tasks import SearchTasks
from taskflow.application.sort_tasks import SortTasks
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
    ) -> Task:
        """Fügt eine Aufgabe hinzu, wenn der Titel nicht leer ist."""
        create_task = CreateTask(self.repository)
        task = create_task.execute(title, priority, due_date)
        logger.info("Aufgabe erstellt: %s", task.title)
        return task

    def remove_task(self, task_id: UUID) -> Task:
        """Entfernt eine Aufgabe anhand ihrer ID."""
        remove_task = RemoveTask(self.repository)
        removed_task = remove_task.execute(task_id)
        logger.info("Aufgabe gelöscht: %s", removed_task.title)
        return removed_task

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

    def sort_tasks(self, field: SortField, reverse: bool = False) -> list[Task]:
        tasks = self.repository.get_all()
        sort_tasks = SortTasks()
        return sort_tasks.execute(tasks, field, reverse)

    def filter_tasks(self, filter_type: FilterType) -> list[Task]:
        tasks = self.repository.get_all()
        filter_tasks = FilterTasks()
        return filter_tasks.execute(tasks, filter_type)

    def search_tasks(self, search_text: str) -> list[Task]:
        tasks = self.repository.get_all()
        search_tasks = SearchTasks()
        return search_tasks.execute(tasks, search_text)

    def get_statistics(self) -> TaskStatistics:
        tasks = self.repository.get_all()
        statistics = GetStatistics()
        return statistics.execute(tasks)
