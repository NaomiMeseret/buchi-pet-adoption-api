from dataclasses import dataclass

from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource


@dataclass(slots=True)
class Pet:
    id: str
    name: str
    pet_type: str
    source: PetSource
    age: int | None = None
    gender: PetGender | None = None
    size: PetSize | None = None
    breed: str | None = None
    description: str | None = None
    good_with_children: bool | None = None
    photo_url: str | None = None
    is_available: bool = True
