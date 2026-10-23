from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from taskflow.database import engine


async def check_database_readiness() -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False
