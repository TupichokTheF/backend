from datetime import datetime

from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    is_seller: Mapped[bool]

    products: Mapped[list["Product"]] = relationship()
    orders: Mapped[list["Order"]] = relationship()

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    product_name: Mapped[str] = mapped_column(nullable=False)
    stock_quantity: Mapped[int]
    description: Mapped[str]
    price: Mapped[float] = mapped_column(nullable=False)

    seller: Mapped["User"] = relationship(back_populates="products")
    order_details: Mapped[list["OrderDetails"]] = relationship()

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    status_id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]

    orders: Mapped[list["Order"]] = relationship()

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("order_statuses.status_id"))
    created_at: Mapped[datetime]

    status: Mapped["OrderStatus"] = relationship(back_populates="orders")
    receiver: Mapped["User"] = relationship(back_populates="orders")
    order_details: Mapped[list["OrderDetails"]] = relationship()

class OrderDetails(Base):
    __tablename__ = "order_details"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates="order_details")
    order: Mapped["Order"] = relationship(back_populates="order_details")


