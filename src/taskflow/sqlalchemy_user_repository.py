from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from taskflow.user import User
from taskflow.user_model import UserModel


class SqlalchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user: User) -> None:
        user_model = UserModel(
            user_id=user.id,
            email=user.email,
            password_hash=user.password_hash,
        )
        self._session.add(user_model)

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        user_model = self._session.scalar(statement)
        if user_model is None:
            return None

        return User(
            email=user_model.email,
            password_hash=user_model.password_hash,
            user_id=user_model.user_id,
        )

    def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(UserModel).where(UserModel.user_id == user_id)
        user_model = self._session.scalar(statement)
        if user_model is None:
            return None

        return User(
            email=user_model.email,
            password_hash=user_model.password_hash,
            user_id=user_model.user_id,
        )
