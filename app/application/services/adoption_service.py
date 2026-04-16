from datetime import datetime, timezone
from uuid import uuid4

from app.core.exceptions import NotFoundError
from app.domain.entities.adoption_request import AdoptionRequest
from app.domain.entities.pet import Pet
from app.domain.interfaces.adoption_repository import AdoptionRepository
from app.domain.interfaces.customer_repository import CustomerRepository
from app.domain.interfaces.external_dog_provider import ExternalDogProvider
from app.domain.interfaces.pet_repository import PetRepository
from app.domain.value_objects.date_range import DateRange


class AdoptionService:
    def __init__(
        self,
        adoption_repository: AdoptionRepository,
        customer_repository: CustomerRepository,
        pet_repository: PetRepository,
        external_dog_provider: ExternalDogProvider,
    ) -> None:
        self.adoption_repository = adoption_repository
        self.customer_repository = customer_repository
        self.pet_repository = pet_repository
        self.external_dog_provider = external_dog_provider

    def create(self, *, customer_id: str, pet_id: str) -> AdoptionRequest:
        customer = self.customer_repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError("customer not found")

        pet = self._get_or_snapshot_pet(pet_id)
        if pet is None:
            raise NotFoundError("pet not found")

        adoption_request = AdoptionRequest(
            id=str(uuid4()),
            customer_id=customer.id,
            pet_id=pet.id,
            created_at=datetime.now(timezone.utc),
        )
        return self.adoption_repository.create(adoption_request)

    def get_by_date_range(self, date_range: DateRange) -> list[dict]:
        adoption_requests = self.adoption_repository.get_by_date_range(date_range)
        items: list[dict] = []

        for adoption_request in adoption_requests:
            customer = self.customer_repository.get_by_id(adoption_request.customer_id)
            pet = self.pet_repository.get_by_id(adoption_request.pet_id)
            if customer is None or pet is None:
                continue

            items.append(
                {
                    "customer_id": customer.id,
                    "customer_phone": customer.phone,
                    "customer_name": customer.name,
                    "pet_id": pet.id,
                    "type": pet.type,
                    "gender": pet.gender,
                    "size": pet.size,
                    "age": pet.age,
                    "good_with_children": pet.good_with_children,
                    "created_at": adoption_request.created_at,
                    "status": adoption_request.status,
                }
            )

        return items

    def _get_or_snapshot_pet(self, pet_id: str) -> Pet | None:
        pet = self.pet_repository.get_by_id(pet_id)
        if pet is not None:
            return pet

        external_pet = self.external_dog_provider.get_by_id(pet_id)
        if external_pet is None:
            return None

        return self.pet_repository.create(external_pet)
