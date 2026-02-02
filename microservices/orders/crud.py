from microservices.orders import models
from microservices.orders.database import database, redis

from sqlalchemy import update

class OrderRepository:

    def add_order(self, user_id: int):
        order = models.Order(receiver_id=user_id)
        with database.session() as session:
            session.add(order)
            session.commit()
            session.refresh(order)
        return order.order_id

    def get_product_cart(self, user_id: int):
        data = redis.hgetall(f"cart:{user_id}")
        return {key.decode(): val.decode() for key, val in data.items()}

    def update_product_quantity(self, product_id: int, quantity: int):
        query = (update(models.Product)
                 .filter_by(product_id = product_id)
                 .filter(models.Product.stock_quantity >= models.Product.stock_quantity - quantity)
                 .values(stock_quantity=models.Product.stock_quantity - quantity))
        with database.session() as session:
            res = session.execute(query)
            if not res.rowcount == 0:
                raise Exception("Недостаточно единиц товара!")
            session.commit()

    def add_order_detail(self, order_id: int, product_id: int, quantity: int):
        order_detail = models.OrderDetails(order_id = order_id, product_id=product_id, quantity=quantity)
        with database.session() as session:
            session.add(order_detail)
            session.commit()

    def delete_product_from_cart(self, user_id: int, product: str):
        redis.hdel(f"cart:{user_id}", product)