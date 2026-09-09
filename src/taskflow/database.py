from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///task.db")

SessionFactory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
