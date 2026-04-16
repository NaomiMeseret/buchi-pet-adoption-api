from abc import ABC, abstractmethod

from app.domain.entities.adoption_request import AdoptionRequest
from app.domain.value_objects.date_range import DateRange


class AdoptionRepository(ABC):
    @abstractmethod
    def get_by_date_range(self, date_range: DateRange) -> list[AdoptionRequest]:
        pass

    @abstractmethod
    def create(self, adoption_request: AdoptionRequest) -> AdoptionRequest:
        pass
