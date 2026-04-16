from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.pet import Pet
from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType
from app.domain.interfaces.pet_repository import PetRepository
from app.domain.value_objects.pet_search_filters import PetSearchFilters
from app.infrastructure.db.models.pet_model import PetModel


class PetRepositorySQLAlchemy(PetRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, pet_id: str) -> Pet | None:
        statement = select(PetModel).where(PetModel.id == pet_id)
        pet_model = self.session.scalar(statement)
        if pet_model is None:
            return None

        return self._to_domain(pet_model)

    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        statement = select(PetModel).where(PetModel.is_available.is_(True))

        if filters.types:
            statement = statement.where(PetModel.type.in_([pet_type.value for pet_type in filters.types]))

        if filters.genders:
            statement = statement.where(PetModel.gender.in_([gender.value for gender in filters.genders]))

        if filters.sizes:
            statement = statement.where(PetModel.size.in_([size.value for size in filters.sizes]))

        if filters.ages:
            statement = statement.where(PetModel.age.in_([age.value for age in filters.ages]))

        if filters.good_with_children is not None:
            statement = statement.where(PetModel.good_with_children == filters.good_with_children)

        statement = statement.order_by(PetModel.id.asc()).limit(limit)
        pet_models = self.session.scalars(statement).all()
        return [self._to_domain(pet_model) for pet_model in pet_models]

    def create(self, pet: Pet) -> Pet:
        pet_model = self._to_model(pet)
        self.session.add(pet_model)
        self.session.commit()
        self.session.refresh(pet_model)
        return self._to_domain(pet_model)

    @staticmethod
    def _to_domain(pet_model: PetModel) -> Pet:
        return Pet(
            id=pet_model.id,
            type=PetType(pet_model.type),
            source=PetSource(pet_model.source),
            photos=list(pet_model.photos or []),
            external_id=pet_model.external_id,
            name=pet_model.name,
            gender=PetGender(pet_model.gender) if pet_model.gender else None,
            size=PetSize(pet_model.size) if pet_model.size else None,
            age=PetAge(pet_model.age) if pet_model.age else None,
            good_with_children=pet_model.good_with_children,
            breed=pet_model.breed,
            description=pet_model.description,
            is_available=pet_model.is_available,
        )

    @staticmethod
    def _to_model(pet: Pet) -> PetModel:
        return PetModel(
            id=pet.id,
            type=pet.type.value,
            source=pet.source.value,
            photos=pet.photos,
            external_id=pet.external_id,
            name=pet.name,
            gender=pet.gender.value if pet.gender else None,
            size=pet.size.value if pet.size else None,
            age=pet.age.value if pet.age else None,
            good_with_children=pet.good_with_children,
            breed=pet.breed,
            description=pet.description,
            is_available=pet.is_available,
        )
