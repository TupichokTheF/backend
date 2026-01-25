from app.database import SessionDep
from sqlalchemy import select, delete
from fastapi import Depends

from app.schemas.tokens import RefreshTokenData
from app.models import RefreshToken

from typing import Annotated

class TokenRepository:

    def __init__(self, session: SessionDep):
        self._session = session

    async def add_refresh_token(self, refresh_token: RefreshTokenData):
        self._session.add(RefreshToken(**refresh_token.model_dump()))
        await self._session.commit()
        return {"status": "Successfully added"}

    async def get_refresh_token(self, refresh_token: str):
        query = select(RefreshToken).filter(RefreshToken.refresh_token == refresh_token)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def delete_refresh_token(self, refresh_token):
        query = delete(RefreshToken).filter_by(refresh_token=refresh_token)
        await self._session.execute(query)
        await self._session.commit()
        return {"Status": "Successfully deleted"}

async def get_token_repository(session: SessionDep):
    return TokenRepository(session)

TokenRepositoryDep = Annotated[TokenRepository, Depends(get_token_repository)]