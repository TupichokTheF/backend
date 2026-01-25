from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models
from app.schemas.user import UserSignup
from app.security import get_password_hash

async def get_user_by_username(session: AsyncSession, username: str):
    query = select(models.User).filter_by(username=username)
    res = await session.execute(query)
    return res.scalars().first()

async def get_user_by_email(session: AsyncSession, email: str):
    query = select(models.User).filter_by(email=email)
    res = await session.execute(query)
    return res.scalars().first()

async def add_user(session: AsyncSession, user_data: UserSignup):
    user_data.password = get_password_hash(user_data.password)
    user = models.User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return {"status": "Successfully added"}

async def all_users(session: AsyncSession):
    query = select(models.User)
    res = await session.execute(query)
    return res.scalars().all()
