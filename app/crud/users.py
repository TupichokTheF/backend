from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from app import models
from app.initialize_database import SessionDep
from app.schemas.user import UserSignup
from app.security import get_password_hash

from typing import Annotated

class UserRepository:

    def __init__(self, session_: SessionDep):
        self._session = session_

    async def get_user_by_username(self, username: str):
        query = select(models.User).filter_by(username=username)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def get_user_by_email(self, email: str):
        query = select(models.User).filter_by(email=email)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def add_user(self, user_data: UserSignup):
        user_data.password = get_password_hash(user_data.password)
        user = models.User(**user_data.model_dump())
        self._session.add(user)
        await self._session.commit()
        return {"status": "Successfully added"}

async def get_user_repository(session: SessionDep):
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
