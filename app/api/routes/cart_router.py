from fastapi import APIRouter, Body

from app.api.services.user_cart import UserCartDep
from app.schemas.cart import AddToCard, IncrementProduct, DeleteProductFromCart


cart_router = APIRouter(
    tags = ["Cart operations"],
    prefix="/cart",
)

@cart_router.post("/add")
async def add_to_cart(user_cart: UserCartDep, product_id: int = Body(embed=True)):
    cart = AddToCard(product_id=product_id)
    return user_cart.add_to_cart(cart)

@cart_router.get("/get")
async def get_user_cart(user_cart: UserCartDep):
    return await user_cart.get_user_cart()

@cart_router.patch("/update_quantity")
async def update_quantity_of_product(user_cart: UserCartDep, cart_data: list[IncrementProduct] = Body(embed=True)):
    user_cart.change_quantity(cart_data)
    return {"status": "updated"}

@cart_router.delete("/delete_product")
async def delete_product(user_cart: UserCartDep, cart_data: DeleteProductFromCart):
    return user_cart.delete_product(cart_data)