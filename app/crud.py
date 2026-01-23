from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

import asyncio

from app import models
from app.initialize_database import engine
from app.api.schemas import PaginatedParams, ProductCreate

async def get_all_products(session: AsyncSession):
    query = select(models.Product)
    res = await session.execute(query)
    return res.scalars().all()

async def get_paginated_products(session: AsyncSession, params: dict[str]):
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

async def main():
    session = async_sessionmaker(engine)
    async with session() as ses:
        Users = await get_all_users(ses)
        print(Users)

if __name__ == "__main__":
    asyncio.run(main())
