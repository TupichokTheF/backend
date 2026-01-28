from fastapi import APIRouter, HTTPException, status, Cookie, Response

from app.api.services.user_service import UserServiceDep
from app.api.services.auth_service import AuthServiceDep
from app.api.deps import AuthorizationDep
from app.schemas.tokens import TokenBase
from app.schemas.user import UserAuthentication, UserSignup, UserResponse

from typing import Annotated

auth_router = APIRouter(
    tags=["Users operations"],
    prefix="/auth"
)

@auth_router.post("/signin")
async def auth_user(auth_service: AuthServiceDep, data: UserAuthentication, response: Response):
    user = await auth_service.authenticate_user(data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await auth_service.generate_token({"sub": user.username})
    refresh_token = await auth_service.generate_refresh_token({"sub": user.username})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60
    )
    return TokenBase(access_token=access_token, token_type="bearer")

@auth_router.post("/signup")
async def signup_user(user_service: UserServiceDep, data: UserSignup):
    try:
        return await user_service.add_user_if_not_exist(data)
    except HTTPException as e:
        raise e

@auth_router.post("/logout")
async def logout_user(auth_service: AuthServiceDep, response: Response, refresh_token: Annotated[str, Cookie()]):
    try:
        token = await auth_service.get_refresh_token(refresh_token)
        await auth_service.delete_refresh_token(token)
        response.delete_cookie("refresh_token")
        return {"detail": "Logged out"}
    except Exception:
        return {"detail": "Refresh token invalid"}

@auth_router.post("/refresh")
async def refresh_user_token(auth_service: AuthServiceDep, refresh_token: Annotated[str, Cookie()]):
    try:
        refresh_token = await auth_service.get_refresh_token(refresh_token)
    except HTTPException as e:
        raise e
    access_token = await auth_service.generate_token({"sub": refresh_token.username})
    return TokenBase(access_token=access_token, token_type="bearer")


@auth_router.get("/user", response_model = UserResponse)
async def get_all_users(current_user: AuthorizationDep):
    return current_user
