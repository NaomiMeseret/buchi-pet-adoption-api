from abc import ABC, abstractmethod

from app.domain.entities.pet import Pet
from app.domain.value_objects.pet_search_filters import PetSearchFilters


class ExternalDogProvider(ABC):
    @abstractmethod
    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        pass

    @abstractmethod
    def get_by_id(self, pet_id: str) -> Pet | None:
        pass
