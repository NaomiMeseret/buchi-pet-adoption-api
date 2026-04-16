from app.api.routes.adoption import router as adoption_router
from app.api.routes.customers import router as customers_router
from app.api.routes.pets import router as pets_router
from app.api.routes.reports import router as reports_router

__all__ = ["pets_router", "customers_router", "adoption_router", "reports_router"]
