from taskflow.async_user_unit_of_work import AsyncUserUnitOfWork
from taskflow.exceptions import DuplicateUserError
from taskflow.password_hasher import PasswordHasher
from taskflow.user import User


class AsyncRegisterUser:
    def __init__(
        self,
        unit_of_work: AsyncUserUnitOfWork,
        password_hasher: PasswordHasher,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    async def execute(self, email: str, password: str) -> None:
        normalized_email = email.strip().lower()
        async with self._unit_of_work:
            if (
                await self._unit_of_work.users.get_by_email(normalized_email)
                is not None
            ):
                raise DuplicateUserError("Der User existiert bereits.")
            password_hash = self._password_hasher.hash(password)
            user = User(
                email=normalized_email,
                password_hash=password_hash,
            )
            await self._unit_of_work.users.add(user)
            await self._unit_of_work.commit()
