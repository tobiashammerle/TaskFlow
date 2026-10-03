from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as JWTInvalidTokenError

from taskflow.exceptions import InvalidTokenError
from taskflow.token_service import TokenService


class JWTTokenService(TokenService):
    def __init__(self, secret: str, access_token_expire_minutes: int) -> None:
        self._secret = secret
        self._access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self._access_token_expire_minutes),
        }
        return jwt.encode(
            payload,
            self._secret,
            algorithm="HS256",
        )

    def decode_access_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=["HS256"],
            )
            return UUID(payload["sub"])
        except JWTInvalidTokenError:
            raise InvalidTokenError("Ungültiger Access Token.") from None
