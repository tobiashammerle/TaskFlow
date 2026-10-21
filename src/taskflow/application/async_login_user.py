from taskflow.application.async_authenticate_user import AsyncAuthenticateUser
from taskflow.token_service import TokenService


class AsyncLoginUser:
    def __init__(
        self, authenticate_user: AsyncAuthenticateUser, token_service: TokenService
    ) -> None:
        self._authenticate_user = authenticate_user
        self._token_service = token_service

    async def execute(self, email: str, password: str) -> str:
        user = await self._authenticate_user.execute(
            email=email,
            password=password,
        )
        return self._token_service.create_access_token(user.id)
