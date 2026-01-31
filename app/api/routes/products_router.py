from fastapi import APIRouter, Depends, Body

from app.api.services.products_service import ProductServiceDep
from app.schemas.products import PaginatedParams, ProductCreate
from app.core.authorization import AuthorizationDep

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

@products_router.post("/add_to_favourite")
async def add_product_to_favourite(product_service: ProductServiceDep, current_user: AuthorizationDep, product_id: int = Body(embed=True)):
    return await product_service.add_to_favourite(current_user.user_id, product_id)

@products_router.get("/favourite_products")
async def get_favourite_products(product_service: ProductServiceDep, current_user: AuthorizationDep):
    favourite_products = await product_service.get_favourite_products(current_user.user_id)
    return list(favourite_products)

@products_router.delete("/delete_favourite")
async def delete_favourite_product(product_service: ProductServiceDep, current_user: AuthorizationDep, product_id: int = Body(embed=True)):
    return await product_service.delete_favourite(current_user.user_id, product_id)