from fastapi import APIRouter

from app.api.services.publisher import RabbitDep
from app.core.authorization import AuthorizationDep

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders operations"]
)

@orders_router.post("/make_order")
async def make_user_order(rabbit: RabbitDep, current_user: AuthorizationDep):
    rabbit.produce_message("orders", {"user_id": current_user.user_id})
    return {"status": "Order made"}
