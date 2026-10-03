from taskflow.exceptions import InvalidCredentialsError
from taskflow.password_hasher import PasswordHasher
from taskflow.user import User
from taskflow.user_unit_of_work import UserUnitOfWork


class AuthenticateUser:
    def __init__(
        self, unit_of_work: UserUnitOfWork, password_hasher: PasswordHasher
    ) -> None:
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    def execute(self, email: str, password: str) -> User:
        normalized_email = email.strip().lower()
        user = self._unit_of_work.users.get_by_email(normalized_email)
        if user is None:
            raise InvalidCredentialsError("Ungültige Zugangsdaten.")
        if not self._password_hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError("Ungültige Zugangsdaten.")
        return user
