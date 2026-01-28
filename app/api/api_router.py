from app.api.routes.products_router import products_router
from app.api.routes.auth_router import auth_router
from app.api.routes.cart_router import cart_router

from fastapi import APIRouter

api_router = APIRouter(
    prefix="/api"
)
api_router.include_router(products_router)
api_router.include_router(auth_router)
api_router.include_router(cart_router)