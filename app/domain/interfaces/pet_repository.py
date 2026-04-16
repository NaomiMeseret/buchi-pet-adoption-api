from abc import ABC, abstractmethod

from app.domain.entities.pet import Pet
from app.domain.value_objects.pet_search_filters import PetSearchFilters


class PetRepository(ABC):
    @abstractmethod
    def get_by_id(self, pet_id: str) -> Pet | None:
        pass

    @abstractmethod
    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        pass

    @abstractmethod
    def create(self, pet: Pet) -> Pet:
        pass
