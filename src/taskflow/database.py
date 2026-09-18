import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///task.db")


engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
