from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer

from pydantic import Field
from typing import Annotated

from app.schemas.user import UserResponse
from app.schemas.tokens import TokenData
from app.core.settings import settings
from app.crud.users import UserRepositoryDep
from app.api.services.auth_service import AuthServiceDep

import jwt
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_rep: UserRepositoryDep):
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
    user = await user_rep.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def check_authorization(auth_service: AuthServiceDep,
                              current_user: Annotated[UserResponse, Depends(get_current_user)],
                              refresh_token: Annotated[str, Cookie()]
                              ):
    try:
        await auth_service.get_username_by_refresh_token(refresh_token)
    except HTTPException as e:
        raise e

    return current_user

async def paginated_params(limit: Annotated[int, Field(20, le=100)], offset: int = 0):
    return {"limit": limit, "offset": offset}

PaginationDep = Annotated[dict, Depends(paginated_params)]
AuthorizationDep = Annotated[UserResponse, Depends(check_authorization)]
