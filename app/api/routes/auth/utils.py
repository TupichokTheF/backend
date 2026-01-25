from app.security import verify_password
from app.settings import settings
from app.crud.users import get_user_by_username
from app.crud.tokens import add_refresh_token
from app.schemas.user import UserAuthentication
from app.schemas.tokens import RefreshTokenData

from datetime import timedelta, datetime, timezone
import jwt

from sqlalchemy.ext.asyncio import AsyncSession


async def authenticate_user(session: AsyncSession, user_: UserAuthentication):
    user = await get_user_by_username(session, user_.username)
    if not user:
        return False
    if not verify_password(user_.password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = settings.ACCESS_TOKEN_EXPIRES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM_OF_CIFER)
    return encoded_jwt

async def create_refresh_token(session: AsyncSession, data: dict, expires_delta: timedelta | None = settings.REFRESH_TOKEN_EXPIRES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM_OF_CIFER)
    refresh_token = RefreshTokenData(refresh_token=encoded_jwt, username=data["sub"], expired_at=expire)
    await add_refresh_token(session, refresh_token)
    return encoded_jwt