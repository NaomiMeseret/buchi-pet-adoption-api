from dataclasses import dataclass

from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType


@dataclass
class Pet:
    id: str
    type: PetType
    source: PetSource
    photos: list[str]
    external_id: str | None = None
    name: str | None = None
    gender: PetGender | None = None
    size: PetSize | None = None
    age: PetAge | None = None
    good_with_children: bool | None = None
    breed: str | None = None
    description: str | None = None
    is_available: bool = True

    def __post_init__(self) -> None:
        if self.source == PetSource.EXTERNAL and not self.external_id:
            self.external_id = self.id
