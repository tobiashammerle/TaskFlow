from taskflow.exceptions import DuplicateUserError
from taskflow.password_hasher import PasswordHasher
from taskflow.user import User
from taskflow.user_unit_of_work import UserUnitOfWork


class RegisterUser:
    def __init__(
        self,
        unit_of_work: UserUnitOfWork,
        password_hasher: PasswordHasher,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    def execute(self, email: str, password: str) -> None:
        normalized_email = email.strip().lower()
        with self._unit_of_work:
            if self._unit_of_work.users.get_by_email(normalized_email) is not None:
                raise DuplicateUserError("Der User existiert bereits.")
            password_hash = self._password_hasher.hash(password)
            user = User(
                email=normalized_email,
                password_hash=password_hash,
            )
            self._unit_of_work.users.add(user)
            self._unit_of_work.commit()
