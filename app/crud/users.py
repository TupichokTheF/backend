from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models

async def get_user_by_username(session: AsyncSession, username: str):
    query = select(models.User).filter_by(username=username)
    res = await session.execute(query)
    return res.scalars().first()
