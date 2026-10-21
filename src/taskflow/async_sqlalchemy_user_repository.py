from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow.user import User
from taskflow.user_model import UserModel


class AsyncSqlalchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> None:
        user_model = UserModel(
            user_id=user.id,
            email=user.email,
            password_hash=user.password_hash,
        )
        self._session.add(user_model)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        user_model = await self._session.scalar(statement)
        if user_model is None:
            return None

        return User(
            email=user_model.email,
            password_hash=user_model.password_hash,
            user_id=user_model.user_id,
        )

    async def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(UserModel).where(UserModel.user_id == user_id)
        user_model = await self._session.scalar(statement)
        if user_model is None:
            return None

        return User(
            email=user_model.email,
            password_hash=user_model.password_hash,
            user_id=user_model.user_id,
        )
