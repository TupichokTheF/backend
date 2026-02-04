from pydantic import BaseModel, Field

class CartDataBase(BaseModel):
    product_id: int

class AddToCard(CartDataBase):
    pass

class IncrementProduct(CartDataBase):
    quantity: int = Field(ge=1, le=99)

class DeleteProductFromCart(CartDataBase):
    pass