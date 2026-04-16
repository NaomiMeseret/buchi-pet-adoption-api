from dataclasses import dataclass
from uuid import uuid4

from app.core.exceptions import BadRequestError
from app.domain.entities.pet import Pet
from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType
from app.domain.interfaces.file_storage import FileStorage
from app.domain.interfaces.pet_repository import PetRepository


@dataclass(frozen=True)
class PetPhotoInput:
    filename: str
    content: bytes


class CreatePetService:
    def __init__(
        self,
        pet_repository: PetRepository,
        file_storage: FileStorage,
    ) -> None:
        self.pet_repository = pet_repository
        self.file_storage = file_storage

    def create(
        self,
        *,
        pet_type: PetType,
        gender: PetGender,
        size: PetSize,
        age: PetAge,
        good_with_children: bool,
        photos: list[PetPhotoInput],
    ) -> Pet:
        if not photos:
            raise BadRequestError("at least one photo is required")

        photo_urls = [
            self.file_storage.save(photo.filename, photo.content)
            for photo in photos
        ]

        pet = Pet(
            id=str(uuid4()),
            type=pet_type,
            source=PetSource.LOCAL,
            photos=photo_urls,
            gender=gender,
            size=size,
            age=age,
            good_with_children=good_with_children,
        )
        return self.pet_repository.create(pet)
