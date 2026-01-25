from fastapi import Depends, HTTPException, status

from app.crud.users import UserRepositoryDep
from app.schemas.user import UserSignup

from typing import Annotated

class UserService:

    def __init__(self, user_rep: UserRepositoryDep):
        self._user_rep = user_rep

    async def add_user_if_not_exist(self, data: UserSignup):
        if await self._user_rep.get_user_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already used"
            )
        if await self._user_rep.get_user_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already used"
            )
        return await self._user_rep.add_user(data)

async def get_user_service(user_rep: UserRepositoryDep):
    return UserService(user_rep)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]