from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from app.initialize_database import engine

import asyncio

from app import models

async def get_all_products(session: AsyncSession):
    query = select(models.User)
    res = await session.execute(query)
    return res.scalar().all()

async def main():
    session = async_sessionmaker(engine)
    async with session() as ses:
        user = models.User(username="Bob", password="1q2w3e", is_seller=True)
        ses.add(user)
        await ses.commit()


if __name__ == "__main__":
    asyncio.run(main())
