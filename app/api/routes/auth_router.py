from fastapi import APIRouter, HTTPException, status, Cookie, Response, Body

from app.api.services.user_service import UserServiceDep
from app.api.services.auth_service import AuthServiceDep
from app.schemas.tokens import TokenBase
from app.schemas.user import UserAuthentication, UserSignup

from typing import Annotated

auth_router = APIRouter(
    tags=["Users operations"],
    prefix="/auth"
)


@auth_router.post("/signin")
async def auth_user(auth_service: AuthServiceDep, data: UserAuthentication):
    user = await auth_service.authenticate_user(data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"detail": "User authenticated"}


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
        username = await auth_service.get_username_by_refresh_token(refresh_token)
        access_token = await auth_service.generate_token({"sub": username})
        return TokenBase(access_token=access_token, token_type="bearer")
    except HTTPException as e:
        raise e


@auth_router.post("/make_two_factor_auth")
async def make_two_factor_auth(auth_service: AuthServiceDep, username: str = Body(embed=True)):
    try:
        await auth_service.send_two_auth_code(username)
        return {"detail": "Код отправлен"}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username",
        )


@auth_router.post("/check_two_factor_auth")
async def check_two_factor_auth(auth_service: AuthServiceDep,
                                response: Response,
                                code: int = Body(embed=True),
                                username: str = Body(embed=True),
                                ):
    try:
        await auth_service.check_two_factor_code(username, code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect code",
        )
    access_token = await auth_service.generate_token({"sub": username})
    refresh_token = await auth_service.generate_refresh_token({"sub": username})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60
    )
    return TokenBase(access_token=access_token, token_type="bearer")
