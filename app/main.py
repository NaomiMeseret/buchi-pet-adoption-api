from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.api.error_handlers import register_exception_handlers
from app.core.config import get_settings
from app.infrastructure.db import Base, engine


settings = get_settings()

app = FastAPI(title="Buchi Pet Adoption API")
app.include_router(api_router)
register_exception_handlers(app)
app.mount(settings.media_url_base, StaticFiles(directory=settings.media_root), name="pet-images")


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
