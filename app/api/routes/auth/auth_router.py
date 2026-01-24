from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.crud.users import get_user_by_username
from app.api.routes.auth.utils import create_access_token, authenticate_user
from app.schemas.tokens import TokenBase

from typing import Annotated

auth_router = APIRouter(
    tags=["Users operations"]
)

@auth_router.post("/auth")
async def get_user(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username})
    return TokenBase(access_token=access_token, token_type="bearer")
