from abc import ABC, abstractmethod

from app.domain.entities.pet import Pet
from app.domain.value_objects.pet_search_filters import PetSearchFilters


class PetRepository(ABC):
    @abstractmethod
    def get_by_id(self, pet_id: str) -> Pet | None:
        """Return one pet by id or None when it does not exist."""

    @abstractmethod
    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        """Search local pets using the provided filters."""

    @abstractmethod
    def exists(self, pet_id: str) -> bool:
        """Return True when the pet exists."""
