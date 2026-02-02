from microservices.orders.crud import OrderRepository


class OrderService:

    def __init__(self):
        self._order_repo = OrderRepository()

    def make_order(self, data: dict):
        order_id = self._order_repo.add_order(data['user_id'])
        product_ids = self._order_repo.get_product_cart(data['user_id'])
        for product, quantity in product_ids.items():
            product_id = product.split(":")[-1]
            try:
                self._order_repo.update_product_quantity(int(product_id), int(quantity))
            except Exception as e:
                self._order_repo.delete_product_from_cart(data["user_id"], product)
                raise e
            self._order_repo.add_order_detail(order_id, int(product_id), int(quantity))


