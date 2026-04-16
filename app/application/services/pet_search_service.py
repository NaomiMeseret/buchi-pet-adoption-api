from app.domain.entities.pet import Pet
from app.domain.interfaces.external_dog_provider import ExternalDogProvider
from app.domain.interfaces.pet_repository import PetRepository
from app.domain.value_objects.pet_search_filters import PetSearchFilters


class PetSearchService:
    def __init__(
        self,
        pet_repository: PetRepository,
        external_dog_provider: ExternalDogProvider,
    ) -> None:
        self.pet_repository = pet_repository
        self.external_dog_provider = external_dog_provider

    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        self._validate_limit(limit)

        local_pets = self.pet_repository.search(filters=filters, limit=limit)
        if len(local_pets) >= limit:
            return local_pets[:limit]

        if not filters.should_search_external_dogs:
            return local_pets

        remaining_limit = limit - len(local_pets)
        external_filters = filters.for_external_dogs()
        external_pets = self.external_dog_provider.search(
            filters=external_filters,
            limit=remaining_limit,
        )

        merged_pets = self._merge_results(local_pets, external_pets)
        return merged_pets[:limit]

    @staticmethod
    def _validate_limit(limit: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

    @staticmethod
    def _merge_results(local_pets: list[Pet], external_pets: list[Pet]) -> list[Pet]:
        local_external_ids = {
            pet.external_id
            for pet in local_pets
            if pet.external_id
        }

        filtered_external_pets = [
            pet
            for pet in external_pets
            if pet.external_id not in local_external_ids
        ]

        return [*local_pets, *filtered_external_pets]
