from app.crud.products import ProductRepositoryDep
from app.schemas.products import PaginatedParams
from app.core.settings import settings

from typing import Annotated
import base64

from fastapi import Depends

class ProductService:

    def __init__(self, product_repo: ProductRepositoryDep):
        self._product_repo = product_repo

    async def get_products(self, params_: PaginatedParams):
        products = await self._product_repo.get_products(params_)
        for i in range(len(products)):
            product = dict(products[i])
            image_path = settings.BASE_DIR + product["path"]
            with open(f"{image_path}", "rb") as image:
                encoded_image = base64.b64encode(image.read()).decode()
            del product["path"]
            product["image"] = encoded_image
            products[i] = product
        return products

async def get_product_service(product_repo: ProductRepositoryDep):
    return ProductService(product_repo)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]