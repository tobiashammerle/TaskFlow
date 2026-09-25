from taskflow.exceptions import DuplicateUserError
from taskflow.password_hasher import PasswordHasher
from taskflow.user import User
from taskflow.user_repository import UserRepository


class RegisterUser:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher

    def execute(self, email: str, password: str) -> None:
        normalized_email = email.strip().lower()
        if self._repository.get_by_email(normalized_email) is not None:
            raise DuplicateUserError("Der User existiert bereits.")
        password_hash = self._password_hasher.hash(password)
        user = User(
            email=normalized_email,
            password_hash=password_hash,
        )
        self._repository.add(user)
