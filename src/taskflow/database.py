import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SYNC_BASE_URL = os.getenv(
    "SYNC_DATABASE_URL",
    "sqlite:///task.db",
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///task.db")


sync_engine = create_engine(SYNC_BASE_URL)
SyncSessionFactory = sessionmaker(bind=sync_engine)


engine = create_async_engine(DATABASE_URL)

SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
