from pathlib import Path

from fastapi import Depends

from taskflow.application.authenticate_user import AuthenticateUser
from taskflow.application.complete_task import CompleteTask
from taskflow.application.create_task import CreateTask
from taskflow.application.filter_tasks import FilterTasks
from taskflow.application.get_tasks import GetTasks
from taskflow.application.login_user import LoginUser
from taskflow.application.register_user import RegisterUser
from taskflow.application.remove_task import RemoveTask
from taskflow.application.search_tasks import SearchTasks
from taskflow.application.sort_tasks import SortTasks
from taskflow.argon2_password_hasher import Argon2PasswordHasher
from taskflow.config import (
    load_access_token_expire_minutes,
    load_jwt_secret,
    load_repository_type,
)
from taskflow.jwt_token_service import JWTTokenService
from taskflow.password_hasher import PasswordHasher
from taskflow.repository_factory import create_repository
from taskflow.repository_type import RepositoryType
from taskflow.repository_unit_of_work import RepositoryUnitOfWork
from taskflow.task_repository import TaskRepository
from taskflow.token_service import TokenService
from taskflow.unit_of_work import UnitOfWork
from taskflow.unit_of_work_factory import create_unit_of_work
from taskflow.user_unit_of_work import UserUnitOfWork


def get_repository() -> TaskRepository:
    repository_type = load_repository_type(Path("settings.ini"))
    repository = create_repository(repository_type)
    return repository


def get_unit_of_work(
    repository: TaskRepository = Depends(get_repository),
) -> UnitOfWork:
    repository_type = load_repository_type(Path("settings.ini"))
    if repository_type == RepositoryType.SQLALCHEMY:
        return create_unit_of_work(repository_type)
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
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetTasks:
    return GetTasks(uow)


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


def get_password_hasher() -> PasswordHasher:
    return Argon2PasswordHasher()


def get_register_user_use_case(
    uow: UserUnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUser:
    return RegisterUser(uow, password_hasher)


def get_authenticate_user_use_case(
    uow: UserUnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthenticateUser:
    return AuthenticateUser(uow, password_hasher)


def get_token_service() -> TokenService:
    return JWTTokenService(
        secret=load_jwt_secret(),
        access_token_expire_minutes=load_access_token_expire_minutes(),
    )


def get_login_user_use_case(
    authenticate_user: AuthenticateUser = Depends(get_authenticate_user_use_case),
    token_service: TokenService = Depends(get_token_service),
) -> LoginUser:
    return LoginUser(authenticate_user, token_service)
