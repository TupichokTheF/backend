from app.api.routes.products.products_router import products_router

from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(products_router)