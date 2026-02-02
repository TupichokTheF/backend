from fastapi import APIRouter

from app.api.services.orders_service import RabbitDep

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders operations"]
)

@orders_router.post("/make_order")
async def make_user_order(rabbit: RabbitDep, user_id: int):
    rabbit.produce_message("orders", {"user_id": user_id})
    return {"status": "Order made"}
