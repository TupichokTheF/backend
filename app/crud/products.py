from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models
from app.schemas.products import PaginatedParams
from app.database import SessionDep

from typing import Annotated

from fastapi import Depends

class ProductRepository:

    def __init__(self, session_: SessionDep):
        self._session = session_

    async def get_products(self, params: PaginatedParams):
        query = (select(models.Product.product_id, models.Product.product_name, models.Product.price, models.Image.path)
                 .join(models.Image, models.Product.image_id==models.Image.image_id)
                 .limit(params.limit)
                 .offset(params.offset))
        res = await self._session.execute(query)
        return res.mappings().all()

async def get_product_repository(session: SessionDep):
    return ProductRepository(session)

ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repository)]

