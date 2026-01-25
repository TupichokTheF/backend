from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer

from pydantic import Field
from typing import Annotated

from app.initialize_database import database
from app.schemas.user import UserResponse
from app.schemas.tokens import TokenData
from app.settings import settings
from app.crud.users import get_user_by_username
from app.crud.tokens import get_refresh_token

import jwt
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

async def paginated_params(limit: Annotated[int, Field(20, le=100)], offset: int = 0):
    return {"limit": limit, "offset": offset}

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM_OF_CIFER])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def check_authorization(session: SessionDep,
                              current_user: Annotated[UserResponse, Depends(get_current_user)],
                              refresh_token: Annotated[str, Cookie()]
                              ):
    refresh_token = await get_refresh_token(session, refresh_token)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user

PaginationDep = Annotated[dict, Depends(paginated_params)]
AuthorizationDep = Annotated[UserResponse, Depends(check_authorization)]
