from dataclasses import dataclass

from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize


@dataclass
class PetSearchFilters:
    pet_type: str | None = None
    age: int | None = None
    gender: PetGender | None = None
    size: PetSize | None = None
    good_with_children: bool | None = None
