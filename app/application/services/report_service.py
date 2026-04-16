from collections import Counter, defaultdict
from datetime import timedelta

from app.domain.interfaces.adoption_repository import AdoptionRepository
from app.domain.interfaces.pet_repository import PetRepository
from app.domain.value_objects.date_range import DateRange


class ReportService:
    def __init__(
        self,
        adoption_repository: AdoptionRepository,
        pet_repository: PetRepository,
    ) -> None:
        self.adoption_repository = adoption_repository
        self.pet_repository = pet_repository

    def generate(self, date_range: DateRange) -> dict:
        adoption_requests = self.adoption_repository.get_by_date_range(date_range)
        adopted_pet_types: Counter[str] = Counter()
        weekly_adoption_requests: dict[str, int] = defaultdict(int)

        for adoption_request in adoption_requests:
            pet = self.pet_repository.get_by_id(adoption_request.pet_id)
            if pet is None:
                continue

            adopted_pet_types[pet.type.value.capitalize()] += 1

            days_from_start = (adoption_request.created_at.date() - date_range.start_date).days
            bucket_offset = max(days_from_start, 0) // 7
            bucket_start = date_range.start_date + timedelta(days=bucket_offset * 7)
            weekly_adoption_requests[bucket_start.isoformat()] += 1

        return {
            "adopted_pet_types": dict(adopted_pet_types),
            "weekly_adoption_requests": dict(sorted(weekly_adoption_requests.items())),
        }
