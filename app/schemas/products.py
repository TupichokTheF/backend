from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seller_id: int
    product_name: str
    description: str
    price: int = Field(1, le=10000)

class ProductCreate(ProductBase):
    stock_quantity: int = Field(1, le=10000)

class PaginatedParams(BaseModel):
    limit: int = Field(ge=20, le=100, default=20)
    offset: int = Field(ge=0, default=0)