from taskflow.application.authenticate_user import AuthenticateUser
from taskflow.token_service import TokenService


class LoginUser:
    def __init__(
        self, authenticate_user: AuthenticateUser, token_service: TokenService
    ) -> None:
        self._authenticate_user = authenticate_user
        self._token_service = token_service

    def execute(self, email: str, password: str) -> str:
        user = self._authenticate_user.execute(
            email=email,
            password=password,
        )
        return self._token_service.create_access_token(user.id)
