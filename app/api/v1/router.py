
from fastapi import APIRouter

from app.api.v1 import customers, orders, returns

api_router = APIRouter()

api_router.include_router(customers.router)
api_router.include_router(orders.router)
api_router.include_router(returns.router)
