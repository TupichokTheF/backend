from app.core.security import verify_password
from app.core.settings import settings
from app.crud.users import UserRepositoryDep
from app.crud.tokens import TokenRepositoryDep
from app.schemas.user import UserAuthentication
from app.api.services.publisher import RabbitDep
from app.database import RedisDep

from datetime import timedelta, datetime, timezone
from typing import Annotated
import jwt, random

from fastapi import Depends, HTTPException, status

class AuthService:
    _ALGORITHM: str = settings.ALGORITHM_OF_CIFER
    _JWT_SECRET_KEY: str = settings.JWT_SECRET_KEY

    def __init__(self, token_rep: TokenRepositoryDep, user_rep: UserRepositoryDep, rabbit_: RabbitDep, redis_: RedisDep):
        self._token_rep = token_rep
        self._user_rep = user_rep
        self._rabbit = rabbit_
        self._redis = redis_

    async def authenticate_user(self, user_: UserAuthentication):
        user = await self._user_rep.get_user_by_username(user_.username)
        if not user:
            return False
        if not verify_password(user_.password, user.password):
            return False
        return user

    async def generate_refresh_token(self, data: dict):
        encoded_jwt = await self.generate_token(data, settings.REFRESH_TOKEN_EXPIRES)
        await self._token_rep.add_refresh_token(encoded_jwt, data["sub"])
        return encoded_jwt

    async def generate_token(self, data: dict, expires_delta: timedelta | None = settings.ACCESS_TOKEN_EXPIRES):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._JWT_SECRET_KEY, algorithm=self._ALGORITHM)
        return encoded_jwt

    async def get_username_by_refresh_token(self, refresh_token: str):
        username = await self._token_rep.get_username_by_refresh_token(refresh_token)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username.decode().split(":")[-1]

    async def delete_refresh_token(self, refresh_token):
        return await self._token_rep.delete_refresh_token(refresh_token)

    async def send_two_auth_code(self, username: str):
        user = await self._user_rep.get_user_by_username(username)
        user_two_auth_code = random.randint(100000, 999999)
        self._redis.set(name=f"two_factor_code:{user.user_id}", value=str(user_two_auth_code), ex=300)
        message = {
            "receiver": user.email,
            "type": "two_factor_auth",
            "title": "Код подтверждения",
            "message": f"Ваш код подтверждения: {user_two_auth_code}"
        }
        self._rabbit.produce_message("two_factor_auth", message)

    async def check_two_factor_code(self, username: str, code: int):
        user = await self._user_rep.get_user_by_username(username)
        user_code = self._redis.get(f"two_factor_code:{user.user_id}").decode()
        if not int(user_code) == code:
            raise Exception("Неверный код!")
        return {"detail": "Аунтефикация проведена"}

async def get_auth_service(token_rep: TokenRepositoryDep, user_rep: UserRepositoryDep, rabbit_: RabbitDep, redis_: RedisDep):
    return AuthService(token_rep, user_rep, rabbit_, redis_)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
