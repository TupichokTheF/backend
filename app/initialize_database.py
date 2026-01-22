from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base
from app.settings import settings

import asyncio

engine = create_async_engine(str(settings.DATABASE_URL))

async def main():
    async with engine.begin() as connection:
        #await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(main())