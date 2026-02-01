from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

from app.models import Base
from app.core.settings import settings

from typing import Annotated

import redis

class DataBase:

    def __init__(self):
        self._engine = create_async_engine(str(settings.DATABASE_URL))
        self._session = async_sessionmaker(self._engine)

    async def get_session(self):
        async with self._session() as ses:
            yield ses

    async def init_database(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def dispose(self):
        await self._engine.dispose()

    @property
    def session(self):
        return self._session()

database = DataBase()
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

def get_redis():
    connection = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return connection

RedisDep = Annotated[redis.Redis, Depends(get_redis)]
