from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import Depends
from pydantic import Field
from typing import Annotated

from app.initialize_database import engine

new_session = async_sessionmaker(engine)

async def get_db():
    async with new_session() as session:
        yield session

async def paginated_params(limit: Annotated[int, Field(20, le=100)], offset: int = 0):
    return {"limit": limit, "offset": offset}

Session = Annotated[AsyncSession, Depends(get_db)]
PaginationDep = Annotated[dict, Depends(paginated_params)]