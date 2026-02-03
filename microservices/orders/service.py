from microservices.orders.crud import OrderRepository


class OrderService:

    def __init__(self):
        self._order_repo = OrderRepository()

    def make_order(self, data: dict):
        product_ids = self._order_repo.get_product_cart(data['user_id'])
        if not product_ids:
            raise Exception("В корзине нет товаров")
        order_details = []
        for product, quantity in product_ids.items():
            product_id = product.split(":")[-1]
            try:
                self._order_repo.update_product_quantity(int(product_id), int(quantity))
            except Exception as e:
                self._order_repo.delete_product_from_cart(data["user_id"], product)
                raise e
            order_details.append((int(product_id), int(quantity)))
        order_id = self._order_repo.add_order(data['user_id'])
        self._order_repo.add_order_detail(order_id, order_details)
        self._order_repo.clear_user_cart(data['user_id'])


