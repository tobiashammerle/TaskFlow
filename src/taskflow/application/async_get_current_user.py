from taskflow.async_user_unit_of_work import AsyncUserUnitOfWork
from taskflow.exceptions import InvalidTokenError
from taskflow.token_service import TokenService
from taskflow.user import User


class AsyncGetCurrentUser:
    def __init__(
        self, unit_of_work: AsyncUserUnitOfWork, token_service: TokenService
    ) -> None:
        self._unit_of_work = unit_of_work
        self._token_service = token_service

    async def execute(self, token: str) -> User:
        user_id = self._token_service.decode_access_token(token)
        async with self._unit_of_work as uow:
            user = await uow.users.get_by_id(user_id)
            if user is None:
                raise InvalidTokenError("Ungültiger Token.")
            return user
