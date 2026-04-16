import os
from dataclasses import dataclass

from app.core.exceptions import BadRequestError


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    thedogapi_api_key: str | None
    media_root: str
    media_url_base: str
    gunicorn_workers: int


def get_settings() -> Settings:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./buchi.db").strip()
    media_root = os.getenv("MEDIA_ROOT", "storage/pet_images").strip()
    media_url_base = os.getenv("MEDIA_URL_BASE", "/media/pet_images").strip()
    app_env = os.getenv("APP_ENV", "development").strip()
    gunicorn_workers = int(os.getenv("GUNICORN_WORKERS", "2"))

    if not database_url:
        raise BadRequestError("DATABASE_URL is required")

    if not media_root:
        raise BadRequestError("MEDIA_ROOT is required")

    if not media_url_base:
        raise BadRequestError("MEDIA_URL_BASE is required")

    return Settings(
        app_env=app_env,
        database_url=database_url,
        thedogapi_api_key=os.getenv("THEDOGAPI_API_KEY"),
        media_root=media_root,
        media_url_base=media_url_base,
        gunicorn_workers=gunicorn_workers,
    )
