from fastapi import APIRouter

from app.api.routes.adoption import router as adoption_router
from app.api.routes.customers import router as customers_router
from app.api.routes.pets import router as pets_router
from app.api.routes.reports import router as reports_router


api_router = APIRouter()
api_router.include_router(pets_router)
api_router.include_router(customers_router)
api_router.include_router(adoption_router)
api_router.include_router(reports_router)
