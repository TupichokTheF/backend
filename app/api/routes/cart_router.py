from fastapi import APIRouter, Depends

from app.api.services.user_cart import UserCartDep
from app.schemas.cart import AddToCard, CartDataBase

from typing import Annotated

cart_router = APIRouter(
    tags = ["Cart operations"],
    prefix="/cart",
)

@cart_router.post("/add")
async def add_to_cart(user_cart: UserCartDep, cart_data: AddToCard):
    return user_cart.add_to_cart(cart_data)

@cart_router.get("/get")
async def get_user_cart(user_cart: UserCartDep, user_id: int):
    return user_cart.get_user_cart(user_id)