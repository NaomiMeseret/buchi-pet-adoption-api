import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

TEST_ROOT = Path(tempfile.gettempdir()) / "buchi_test_runtime"
TEST_ROOT.mkdir(parents=True, exist_ok=True)
(TEST_ROOT / "media").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_ROOT / 'app_startup.db'}")
os.environ.setdefault("MEDIA_ROOT", str(TEST_ROOT / "media"))
os.environ.setdefault("MEDIA_URL_BASE", "/media/pet_images")
os.environ.setdefault("APP_ENV", "test")

from app.api.deps import get_db_session, get_external_dog_provider, get_settings_dependency
from app.core.config import Settings
from app.domain.entities.pet import Pet
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType
from app.domain.value_objects.pet_search_filters import PetSearchFilters
from app.infrastructure.db import Base
from app.main import app


class FakeExternalDogProvider:
    def __init__(self) -> None:
        self.search_results: list[Pet] = []
        self.pet_by_id: dict[str, Pet] = {}

    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        return self.search_results[:limit]

    def get_by_id(self, pet_id: str) -> Pet | None:
        return self.pet_by_id.get(pet_id)


@pytest.fixture
def db_session_factory(tmp_path: Path):
    db_path = tmp_path / "test.sqlite3"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def external_provider() -> FakeExternalDogProvider:
    provider = FakeExternalDogProvider()
    provider.search_results = [
        Pet(
            id="external_dog_100",
            external_id="100",
            type=PetType.DOG,
            source=PetSource.EXTERNAL,
            photos=["https://example.com/dog-100.jpg"],
            size=PetSize.MEDIUM,
        ),
        Pet(
            id="external_dog_101",
            external_id="101",
            type=PetType.DOG,
            source=PetSource.EXTERNAL,
            photos=["https://example.com/dog-101.jpg"],
            size=PetSize.SMALL,
        ),
    ]
    provider.pet_by_id = {pet.id: pet for pet in provider.search_results}
    return provider


@pytest.fixture
def client(
    db_session_factory,
    external_provider: FakeExternalDogProvider,
    tmp_path: Path,
) -> Generator[TestClient, None, None]:
    media_root = tmp_path / "media"
    media_root.mkdir(parents=True, exist_ok=True)

    settings = Settings(
        app_env="test",
        database_url=f"sqlite:///{tmp_path / 'test.sqlite3'}",
        thedogapi_api_key="test-key",
        media_root=str(media_root),
        media_url_base="/media/pet_images",
        gunicorn_workers=1,
    )

    def override_get_db_session() -> Generator[Session, None, None]:
        session = db_session_factory()
        try:
            yield session
        finally:
            session.close()

    def override_get_settings() -> Settings:
        return settings

    def override_get_external_provider() -> FakeExternalDogProvider:
        return external_provider

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_settings_dependency] = override_get_settings
    app.dependency_overrides[get_external_dog_provider] = override_get_external_provider

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
