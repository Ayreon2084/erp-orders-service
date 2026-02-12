from fastapi import APIRouter

from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.clients import router as clients_router
from app.api.v1.endpoints.orders import router as orders_router
from app.api.v1.endpoints.products import router as products_router


api_v1_router = APIRouter()

api_v1_router.include_router(categories_router)
api_v1_router.include_router(clients_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(products_router)
