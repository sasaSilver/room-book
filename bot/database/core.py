from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.config import settings

engine = create_async_engine(
    settings.db_uri,
    pool_pre_ping=True,
    echo=settings.sql_echo
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

def inject_session(func):
    """
    Injects session object to the decorated db method.
    You do not need to pass it manually.
    """

    @wraps(func)
    async def wrapper(*args):
        async with async_session() as session:
            try:
                session.begin()
                return await func(session, *args)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.commit()
                await session.close()

    return wrapper