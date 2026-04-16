from app.domain.interfaces.adoption_repository import AdoptionRepository
from app.domain.interfaces.customer_repository import CustomerRepository
from app.domain.interfaces.external_dog_provider import ExternalDogProvider
from app.domain.interfaces.file_storage import FileStorage
from app.domain.interfaces.pet_repository import PetRepository

__all__ = [
    "PetRepository",
    "CustomerRepository",
    "AdoptionRepository",
    "ExternalDogProvider",
    "FileStorage",
]
