from app.database import RedisDep
from app.schemas.cart import AddToCard, IncrementProduct
from app.api.services.products_service import ProductServiceDep
from app.core.authorization import AuthorizationDep

from typing import Annotated

from fastapi import Depends

class UserCart:

    def __init__(self, redis: RedisDep, product_service: ProductServiceDep, current_user: AuthorizationDep):
        self.conn = redis
        self._product_service = product_service
        self._user = current_user

    def add_to_cart(self, cart_data: AddToCard):
        cart_name = f"cart:{self._user.user_id}"
        return self.conn.hset(cart_name, key=f"product:{cart_data.product_id}", value="1")

    def change_quantity(self, cart_data: list[IncrementProduct]):
        cart_name = f"cart:{self._user.user_id}"
        for cart_changes in cart_data:
            self.conn.hset(cart_name, key=f"product:{cart_changes.product_id}", value=str(cart_changes.quantity))

    async def get_user_cart(self):
        cart_name = f"cart:{self._user.user_id}"
        product_ids, product_vals = self.conn.hkeys(cart_name), self.conn.hvals(cart_name)
        products = await self._product_service.get_list_of_products_by_ids(product_ids)
        for product, product_val in zip(products, product_vals):
            product['quantity'] = product_val
        return products

def get_user_cart(redis: RedisDep, product_serv: ProductServiceDep, current_user: AuthorizationDep):
    return UserCart(redis, product_serv, current_user)

UserCartDep = Annotated[UserCart, Depends(get_user_cart)]

