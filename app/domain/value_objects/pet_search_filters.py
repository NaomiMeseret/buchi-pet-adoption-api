from dataclasses import dataclass, field

from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_type import PetType


@dataclass(frozen=True)
class PetSearchFilters:
    types: tuple[PetType, ...] = field(default_factory=tuple)
    genders: tuple[PetGender, ...] = field(default_factory=tuple)
    sizes: tuple[PetSize, ...] = field(default_factory=tuple)
    ages: tuple[PetAge, ...] = field(default_factory=tuple)
    good_with_children: bool | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "types", self._unique(self.types))
        object.__setattr__(self, "genders", self._unique(self.genders))
        object.__setattr__(self, "sizes", self._unique(self.sizes))
        object.__setattr__(self, "ages", self._unique(self.ages))

    @property
    def should_search_external_dogs(self) -> bool:
        return PetType.DOG in self.types

    def for_external_dogs(self) -> "PetSearchFilters":
        sizes = self.sizes
        if not self.should_search_external_dogs:
            sizes = ()

        return PetSearchFilters(
            types=(PetType.DOG,) if self.should_search_external_dogs else (),
            sizes=sizes,
        )

    @staticmethod
    def _unique(values: tuple) -> tuple:
        return tuple(dict.fromkeys(values))
