from app.crud.products import ProductRepositoryDep
from app.schemas.products import PaginatedParams, ProductCreate
from app.core.settings import settings
from app.database import RedisDep

from typing import Annotated, Iterator
import base64

from fastapi import Depends

class ProductService:

    def __init__(self, product_repo: ProductRepositoryDep, redis_: RedisDep):
        self._redis = redis_
        self._product_repo = product_repo

    async def get_products(self, params_: PaginatedParams):
        products = await self._product_repo.get_products(params_)
        for i in range(len(products)):
            product = dict(products[i])
            await self._replace_image_by_path(product)
            products[i] = product
        return products

    async def get_popular_products(self):
        popular_products: Iterator = reversed(self._redis.zrange(name="score", start=0, end=-1))
        response = await self.get_list_of_products_by_ids(list(popular_products))
        return response

    async def get_favourite_products(self, user_id: int):
        favourite_products = list(self._redis.smembers(f"favourite_products:{user_id}"))
        response = await self.get_list_of_products_by_ids(favourite_products)
        return response

    async def get_list_of_products_by_ids(self, list_of_products: list[bytes]):
        response: list = []
        for product in list_of_products:
            product_id = product.decode().split('product:')[1]
            product_data = dict(await self._product_repo.get_product_by_id(int(product_id)))
            await self._replace_image_by_path(product_data)
            response.append(product_data)
        return response

    async def _replace_image_by_path(self, product: dict):
        image_path = settings.BASE_DIR + product["path"]
        with open(f"{image_path}", "rb") as image:
            encoded_image = base64.b64encode(image.read()).decode()
        del product["path"]
        product["image"] = encoded_image

    async def add_product(self, product: ProductCreate):
        image_path = self._create_image(product.image)
        image_id = await self._product_repo.add_image(image_path)
        product.image_id = image_id
        product_id = await self._product_repo.add_product(product)
        self._redis.zadd(name="score", mapping={f"product:{product_id}": 1})
        return {"status": "Successfully added"}

    def _create_image(self, image_encoded: str):
        decoded_image = base64.b64decode(image_encoded)
        total_count_images = self._redis.incr("total_count_products")
        image_path = f"/images/product{total_count_images - 1}.jpg"
        with open(settings.BASE_DIR + image_path, "wb") as file:
            file.write(decoded_image)
        return image_path

    async def add_to_favourite(self, user_id: int, product_id: int):
        return self._redis.sadd(f"favourite_products:{user_id}", f"product:{product_id}")

    async def delete_favourite(self, user_id, product_id):
        return self._redis.srem(f"favourite_products:{user_id}", f"product:{product_id}")

async def get_product_service(product_repo: ProductRepositoryDep, redis_: RedisDep):
    return ProductService(product_repo, redis_)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]