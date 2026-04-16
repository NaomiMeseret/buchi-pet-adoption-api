from typing import Literal

from pydantic import BaseModel, Field

from app.domain.entities.pet import Pet
from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType
from app.domain.value_objects.pet_search_filters import PetSearchFilters


class CreatePetRequest(BaseModel):
    type: PetType
    gender: PetGender
    size: PetSize
    age: PetAge
    good_with_children: bool


class CreatePetResponseData(BaseModel):
    pet_id: str


class CreatePetResponse(BaseModel):
    status: Literal["success"] = "success"
    data: CreatePetResponseData


class GetPetsQuery(BaseModel):
    types: list[PetType] = Field(default_factory=list)
    genders: list[PetGender] = Field(default_factory=list)
    sizes: list[PetSize] = Field(default_factory=list)
    ages: list[PetAge] = Field(default_factory=list)
    good_with_children: bool | None = None
    limit: int = Field(..., gt=0)

    def to_filters(self) -> PetSearchFilters:
        return PetSearchFilters(
            types=tuple(self.types),
            genders=tuple(self.genders),
            sizes=tuple(self.sizes),
            ages=tuple(self.ages),
            good_with_children=self.good_with_children,
        )


class PetItemResponse(BaseModel):
    pet_id: str
    source: str
    type: str
    gender: str | None = None
    size: str | None = None
    age: str | None = None
    good_with_children: bool | None = None
    photos: list[str]

    @classmethod
    def from_domain(cls, pet: Pet) -> "PetItemResponse":
        return cls(
            pet_id=pet.id,
            source=pet.source.value,
            type=pet.type.value.capitalize(),
            gender=pet.gender.value if pet.gender else None,
            size=pet.size.value if pet.size else None,
            age=pet.age.value if pet.age else None,
            good_with_children=pet.good_with_children,
            photos=pet.photos,
        )


class GetPetsResponseData(BaseModel):
    pets: list[PetItemResponse]


class GetPetsResponse(BaseModel):
    status: Literal["success"] = "success"
    data: GetPetsResponseData
