from app.core.security import verify_password
from app.core.settings import settings
from app.crud.users import UserRepositoryDep
from app.crud.tokens import TokenRepositoryDep
from app.schemas.user import UserAuthentication
from app.schemas.tokens import RefreshTokenData

from datetime import timedelta, datetime, timezone
from typing import Annotated
import jwt

from fastapi import Depends, HTTPException, status

class AuthService:
    _ALGORITHM: str = settings.ALGORITHM_OF_CIFER
    _JWT_SECRET_KEY: str = settings.JWT_SECRET_KEY

    def __init__(self, token_rep: TokenRepositoryDep, user_rep: UserRepositoryDep):
        self._token_rep = token_rep
        self._user_rep = user_rep

    async def authenticate_user(self, user_: UserAuthentication):
        user = await self._user_rep.get_user_by_username(user_.username)
        if not user:
            return False
        if not verify_password(user_.password, user.password):
            return False
        return user

    async def generate_refresh_token(self, data: dict):
        encoded_jwt = await self.generate_token(data, settings.REFRESH_TOKEN_EXPIRES)
        refresh_token = RefreshTokenData(refresh_token=encoded_jwt, username=data["sub"],
                                         expired_at=datetime.now(timezone.utc) + settings.REFRESH_TOKEN_EXPIRES)
        await self._token_rep.add_refresh_token(refresh_token)
        return encoded_jwt

    async def generate_token(self, data: dict, expires_delta: timedelta | None = settings.ACCESS_TOKEN_EXPIRES):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._JWT_SECRET_KEY, algorithm=self._ALGORITHM)
        return encoded_jwt

    async def get_refresh_token(self, refresh_token_: str):
        token = await self._token_rep.get_refresh_token(refresh_token_)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token.refresh_token

    async def delete_refresh_token(self, refresh_token):
        return await self._token_rep.delete_refresh_token(refresh_token)

async def get_auth_service(token_rep: TokenRepositoryDep, user_rep: UserRepositoryDep):
    return AuthService(token_rep, user_rep)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
