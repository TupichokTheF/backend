from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models
from app.schemas.products import PaginatedParams, ProductCreate
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

    async def get_product_by_id(self, product_id: int):
        query = (select(models.Product.product_id, models.Product.product_name, models.Product.price, models.Image.path)
                 .join(models.Image, models.Product.image_id == models.Image.image_id)
                 .filter(models.Product.product_id==product_id))
        res = await self._session.execute(query)
        return res.mappings().first()

    async def add_image(self, image_path: str):
        image = models.Image(path=image_path)
        self._session.add(image)
        await self._session.commit()
        await self._session.refresh(image)
        return image.image_id

    async def add_product(self, product: ProductCreate):
        product = models.Product(**product.model_dump(exclude={"image"}))
        self._session.add(product)
        await self._session.commit()
        await self._session.refresh(product)
        return product.product_id

async def get_product_repository(session: SessionDep):
    return ProductRepository(session)

ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repository)]

