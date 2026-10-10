from taskflow.exceptions import InvalidTokenError
from taskflow.token_service import TokenService
from taskflow.user import User
from taskflow.user_unit_of_work import UserUnitOfWork


class GetCurrentUser:
    def __init__(
        self, unit_of_work: UserUnitOfWork, token_service: TokenService
    ) -> None:
        self._unit_of_work = unit_of_work
        self._token_service = token_service

    def execute(self, token: str) -> User:
        user_id = self._token_service.decode_access_token(token)
        with self._unit_of_work as uow:
            user = uow.users.get_by_id(user_id)
            if user is None:
                raise InvalidTokenError("Ungültiger Token.")
            return user
