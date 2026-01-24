from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Base
from app.settings import settings

class DataBase:

    def __init__(self):
        self.engine = create_async_engine(str(settings.DATABASE_URL))
        self.session = async_sessionmaker(self.engine)

    async def get_session(self):
        async with self.session() as ses:
            yield ses

    async def init_database(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def dispose(self):
        await self.engine.dispose()

database = DataBase()