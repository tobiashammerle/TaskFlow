from pathlib import Path

from fastapi import Depends

from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.filter_tasks import FilterTasks
from taskflow.application.get_tasks import GetTasks
from taskflow.application.remove_task import RemoveTask
from taskflow.application.search_tasks import SearchTasks
from taskflow.application.sort_tasks import SortTasks
from taskflow.config import load_repository_type
from taskflow.repository_factory import create_repository
from taskflow.repository_unit_of_work import RepositoryUnitOfWork
from taskflow.task_repository import TaskRepository
from taskflow.unit_of_work import UnitOfWork


def get_repository() -> TaskRepository:
    repository_type = load_repository_type(Path("settings.ini"))
    repository = create_repository(repository_type)
    return repository


def get_unit_of_work(
    repository: TaskRepository = Depends(get_repository),
) -> UnitOfWork:
    return RepositoryUnitOfWork(repository)


def get_create_task_use_case(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateTask:
    return CreateTask(uow)


def get_remove_task_use_case(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RemoveTask:
    return RemoveTask(uow)


def get_get_tasks_use_case(
    repository: TaskRepository = Depends(get_repository),
) -> GetTasks:
    return GetTasks(repository)


def get_complete_task_use_case(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CompleteTask:
    return CompleteTask(uow)


def get_search_tasks_use_case() -> SearchTasks:
    return SearchTasks()


def get_filter_tasks_use_case() -> FilterTasks:
    return FilterTasks()


def get_sort_tasks_use_case() -> SortTasks:
    return SortTasks()
