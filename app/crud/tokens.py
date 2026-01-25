from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.schemas.tokens import RefreshTokenData
from app.models import RefreshToken


async def add_refresh_token(session: AsyncSession, refresh_token: RefreshTokenData):
    session.add(RefreshToken(**refresh_token.model_dump()))
    await session.commit()
    return {"status": "Successfully added"}

async def get_refresh_token(session: AsyncSession, refresh_token: str):
    query = select(RefreshToken).filter(RefreshToken.refresh_token == refresh_token)
    res = await session.execute(query)
    return res.scalar_one_or_none()

async def delete_refresh_token(session: AsyncSession, refresh_token: str):
    query = delete(RefreshToken).filter_by(refresh_token=refresh_token)
    await session.execute(query)
    await session.commit()
    return {"Status": "Successfully deleted"}