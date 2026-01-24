from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models
from app.schemas.products import ProductCreate

async def get_all_products(session: AsyncSession):
    query = select(models.Product)
    res = await session.execute(query)
    return res.scalars().all()

async def get_paginated_products(session: AsyncSession, params: dict[str, int]):
    query = select(models.Product).limit(params["limit"]).offset(params["offset"])
    res = await session.execute(query)
    return res.scalars().all()

async def add_product(session: AsyncSession, product_data: ProductCreate):
    try:
        product = models.Product(**product_data.model_dump())
        session.add(product)
        await session.commit()
        return {"status": "Successfully added"}
    except Exception as e:
        raise e
