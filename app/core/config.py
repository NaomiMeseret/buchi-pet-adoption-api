import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    thedogapi_api_key: str | None
    media_root: str
    media_url_base: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./buchi.db"),
        thedogapi_api_key=os.getenv("THEDOGAPI_API_KEY"),
        media_root=os.getenv("MEDIA_ROOT", "storage/pet_images"),
        media_url_base=os.getenv("MEDIA_URL_BASE", "/media/pet_images"),
    )
