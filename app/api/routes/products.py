from fastapi import APIRouter, HTTPException, status, Depends

from typing import Annotated

from app.api.deps import Session, PaginationDep
from app.api.schemas import ProductCreate
from app.crud import get_paginated_products, add_product

products_router = APIRouter(tags = ["Products"])

@products_router.get("/products", description="Получение всех продуктов в базе данных")
async def get_products(session: Session, params: PaginationDep):
    return await get_paginated_products(session, params)

@products_router.post("/add_product", description = "Добавление нового продукта")
async def create_product(session: Session, product: ProductCreate):
    try:
        return await add_product(session, product)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка данных"
        )

