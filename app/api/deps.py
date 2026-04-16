from collections.abc import Generator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services import (
    AdoptionService,
    CreatePetService,
    CustomerService,
    PetSearchService,
    ReportService,
)
from app.core.config import Settings, get_settings
from app.domain.interfaces.file_storage import FileStorage
from app.infrastructure.db.session import get_db_session
from app.infrastructure.integrations.thedogapi.client import TheDogApiClient
from app.infrastructure.integrations.thedogapi.provider import TheDogApiExternalDogProvider
from app.infrastructure.repositories.adoption_repository_sqlalchemy import AdoptionRepositorySQLAlchemy
from app.infrastructure.repositories.customer_repository_sqlalchemy import CustomerRepositorySQLAlchemy
from app.infrastructure.repositories.pet_repository_sqlalchemy import PetRepositorySQLAlchemy
from app.infrastructure.storage.local_file_storage import LocalFileStorage


@lru_cache
def get_cached_settings() -> Settings:
    return get_settings()


def get_settings_dependency() -> Settings:
    return get_cached_settings()


def get_pet_repository(session: Session = Depends(get_db_session)) -> PetRepositorySQLAlchemy:
    return PetRepositorySQLAlchemy(session)


def get_customer_repository(session: Session = Depends(get_db_session)) -> CustomerRepositorySQLAlchemy:
    return CustomerRepositorySQLAlchemy(session)


def get_adoption_repository(session: Session = Depends(get_db_session)) -> AdoptionRepositorySQLAlchemy:
    return AdoptionRepositorySQLAlchemy(session)


def get_file_storage(settings: Settings = Depends(get_settings_dependency)) -> FileStorage:
    return LocalFileStorage(
        root_directory=settings.media_root,
        base_url=settings.media_url_base,
    )


def get_external_dog_provider(
    settings: Settings = Depends(get_settings_dependency),
) -> Generator[TheDogApiExternalDogProvider, None, None]:
    client = TheDogApiClient(api_key=settings.thedogapi_api_key)
    try:
        yield TheDogApiExternalDogProvider(client)
    finally:
        client.close()


def get_create_pet_service(
    pet_repository: PetRepositorySQLAlchemy = Depends(get_pet_repository),
    file_storage: FileStorage = Depends(get_file_storage),
) -> CreatePetService:
    return CreatePetService(
        pet_repository=pet_repository,
        file_storage=file_storage,
    )


def get_pet_search_service(
    pet_repository: PetRepositorySQLAlchemy = Depends(get_pet_repository),
    external_dog_provider: TheDogApiExternalDogProvider = Depends(get_external_dog_provider),
) -> PetSearchService:
    return PetSearchService(
        pet_repository=pet_repository,
        external_dog_provider=external_dog_provider,
    )


def get_customer_service(
    customer_repository: CustomerRepositorySQLAlchemy = Depends(get_customer_repository),
) -> CustomerService:
    return CustomerService(customer_repository=customer_repository)


def get_adoption_service(
    adoption_repository: AdoptionRepositorySQLAlchemy = Depends(get_adoption_repository),
    customer_repository: CustomerRepositorySQLAlchemy = Depends(get_customer_repository),
    pet_repository: PetRepositorySQLAlchemy = Depends(get_pet_repository),
    external_dog_provider: TheDogApiExternalDogProvider = Depends(get_external_dog_provider),
) -> AdoptionService:
    return AdoptionService(
        adoption_repository=adoption_repository,
        customer_repository=customer_repository,
        pet_repository=pet_repository,
        external_dog_provider=external_dog_provider,
    )


def get_report_service(
    adoption_repository: AdoptionRepositorySQLAlchemy = Depends(get_adoption_repository),
    pet_repository: PetRepositorySQLAlchemy = Depends(get_pet_repository),
) -> ReportService:
    return ReportService(
        adoption_repository=adoption_repository,
        pet_repository=pet_repository,
    )
