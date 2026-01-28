from fastapi import APIRouter, HTTPException, status, Depends

from app.api.services.products_service import ProductServiceDep
from app.schemas.products import PaginatedParams

products_router = APIRouter(
    tags = ["Products"],
    prefix="/products"
)

@products_router.get("/get_products", description="Получить все продукты")
async def get_all_products(product_service: ProductServiceDep, params: PaginatedParams = Depends()):
    return await product_service.get_products(params)

