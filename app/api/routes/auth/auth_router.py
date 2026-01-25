from fastapi import APIRouter, HTTPException, status, Cookie, Response

from app.api.deps import SessionDep, AuthorizationDep
from app.crud.users import get_user_by_email, get_user_by_username, add_user
from app.crud.tokens import delete_refresh_token, get_refresh_token
from app.api.routes.auth.utils import create_access_token, authenticate_user, create_refresh_token
from app.schemas.tokens import TokenBase
from app.schemas.user import UserAuthentication, UserSignup, UserResponse

from typing import Annotated

auth_router = APIRouter(
    tags=["Users operations"]
)

@auth_router.post("/auth")
async def auth_user(session: SessionDep, data: UserAuthentication, response: Response):
    user = await authenticate_user(session, data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.username})
    refresh_token = await create_refresh_token(session, {"sub": user.username})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60
    )
    return TokenBase(access_token=access_token, token_type="bearer")

@auth_router.post("/signup")
async def signup_user(session: SessionDep, data: UserSignup):
    if not await get_user_by_email(session, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already used"
        )
    if not await get_user_by_username(session, data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already used"
        )
    return await add_user(session, data)

@auth_router.post("/logout")
async def logout_user(session: SessionDep, response: Response, refresh_token: Annotated[str, Cookie()]):
    refresh_token = await get_refresh_token(session, refresh_token)
    if not refresh_token:
        return {"detail": "Refresh token invalid"}
    await delete_refresh_token(session, refresh_token)
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}

@auth_router.post("/refresh")
async def refresh_user_token(session: SessionDep, refresh_token: Annotated[str, Cookie()]):
    refresh_token = await get_refresh_token(session, refresh_token)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": refresh_token.username})
    return TokenBase(access_token=access_token, token_type="bearer")


@auth_router.get("/user", response_model = UserResponse)
async def get_all_users(current_user: AuthorizationDep):
    return current_user
