from types import TracebackType
from uuid import UUID

from taskflow.task import Task
from taskflow.task_repository import TaskRepository
from taskflow.user import User


class FakeTaskRepository:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def save(self, tasks: list[Task]) -> None:
        self.tasks = tasks.copy()

    def get_all(self) -> list[Task]:
        return self.tasks.copy()

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def delete(self, task_id: UUID) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def update(self, task: Task) -> None:
        for i, existing_task in enumerate(self.tasks):
            if existing_task.id == task.id:
                self.tasks[i] = task
                break

    def get_by_id(self, task_id: UUID) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


class FakeUnitOfWork:
    def __init__(self, tasks: TaskRepository | None = None) -> None:
        self.tasks: TaskRepository = tasks or FakeTaskRepository()
        self.committed = False

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


class FakePasswordHasher:
    def hash(self, password: str) -> str:
        return f"hashed-{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == self.hash(password)


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: list[User] = []

    def add(self, user: User) -> None:
        self.users.append(user)

    def get_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None
