from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from bot.settings import settings

DATABASE_URL = settings.db_url.replace('postgresql://', 'postgresql+asyncpg://')

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

"""
Not sure wtf this is
"""
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

"""
For automatic beginning, committing and rolling back of db operations
(whatever that means)
"""
class AsyncSessionManager:
    async def __aenter__(self) -> AsyncSession:
        self.session = async_session()
        self.session.begin()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
