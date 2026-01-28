from app.database import RedisDep
from app.schemas.cart import AddToCard, IncrementProduct, CartDataBase

from typing import Annotated

from fastapi import Depends

class UserCart:

    def __init__(self, redis: RedisDep):
        self.conn = redis

    def add_to_cart(self, cart_data: AddToCard):
        cart_name = f"cart:{cart_data.user_id}"
        return self.conn.hset(cart_name, key=f"product:{cart_data.product_id}", value="1")

    def increment_quantity(self, cart_data: IncrementProduct):
        cart_name = f"cart:{cart_data.user_id}"
        return self.conn.hincrby(cart_name, key=f"product:{cart_data.product_id}", amount=cart_data.quantity)

    def get_user_cart(self, user_id: int):
        cart_name = f"cart:{user_id}"
        return self.conn.hgetall(cart_name)

def get_user_cart(redis: RedisDep):
    return UserCart(redis)

UserCartDep = Annotated[UserCart, Depends(get_user_cart)]

