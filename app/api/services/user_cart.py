from app.database import RedisDep
from app.schemas.cart import AddToCard, IncrementProduct, DeleteProductFromCart
from app.api.services.products_service import ProductServiceDep
from app.core.authorization import AuthorizationDep

from typing import Annotated

from fastapi import Depends

class UserCart:

    def __init__(self, redis: RedisDep, product_service: ProductServiceDep, current_user: AuthorizationDep):
        self._redis = redis
        self._product_service = product_service
        self._cart_name = f"cart:{current_user.user_id}"

    def add_to_cart(self, cart_data: AddToCard):
        return self._redis.hset(self._cart_name, key=f"product:{cart_data.product_id}", value="1")

    def change_quantity(self, cart_data: list[IncrementProduct]):
        for cart_changes in cart_data:
            self._redis.hset(self._cart_name, key=f"product:{cart_changes.product_id}", value=str(cart_changes.quantity))

    def delete_product(self, cart_data: DeleteProductFromCart):
        return self._redis.hdel(self._cart_name, f"product:{cart_data.product_id}")

    async def get_user_cart(self):
        product_ids, product_vals = self._redis.hkeys(self._cart_name), self._redis.hvals(self._cart_name)
        products = await self._product_service.get_list_of_products_by_ids(product_ids)
        for product, product_val in zip(products, product_vals):
            product['quantity'] = product_val
        return products

def get_user_cart(redis: RedisDep, product_serv: ProductServiceDep, current_user: AuthorizationDep):
    return UserCart(redis, product_serv, current_user)

UserCartDep = Annotated[UserCart, Depends(get_user_cart)]
