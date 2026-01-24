from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from pydantic import Field
from typing import Annotated

from app.initialize_database import database

async def paginated_params(limit: Annotated[int, Field(20, le=100)], offset: int = 0):
    return {"limit": limit, "offset": offset}

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
PaginationDep = Annotated[dict, Depends(paginated_params)]