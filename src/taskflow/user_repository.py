from typing import Protocol

from taskflow.user import User


class UserRepository(Protocol):
    def add(self, user: User) -> None: ...

    def get_by_email(self, email: str) -> User | None: ...
