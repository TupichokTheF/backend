from fastapi import APIRouter, HTTPException, status, Depends

from app.api.services.products_service import ProductServiceDep
from app.schemas.products import PaginatedParams, ProductCreate
from app.api.deps import AuthorizationDep

products_router = APIRouter(
    tags = ["Products"],
    prefix="/products"
)

@products_router.get("/get_products", description="Получить все продукты")
async def get_all_products(product_service: ProductServiceDep, params: PaginatedParams = Depends()):
    return await product_service.get_products(params)

@products_router.get("/get_popular_products", description="Получить все продукты")
async def get_popular_products(product_service: ProductServiceDep):
    return await product_service.get_popular_products()

@products_router.post("/create_product", description="Создание продукта")
async def add_product(product_service: ProductServiceDep, current_user: AuthorizationDep, product: ProductCreate):
    product.seller_id = current_user.user_id
    return await product_service.add_product(product)
