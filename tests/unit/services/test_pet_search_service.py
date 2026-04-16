from unittest.mock import Mock

from app.application.services.pet_search_service import PetSearchService
from app.domain.entities.pet import Pet
from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType
from app.domain.interfaces.external_dog_provider import ExternalDogProvider
from app.domain.interfaces.pet_repository import PetRepository
from app.domain.value_objects.pet_search_filters import PetSearchFilters


def make_pet(
    pet_id: str,
    *,
    pet_type: PetType = PetType.DOG,
    source: PetSource = PetSource.LOCAL,
    external_id: str | None = None,
) -> Pet:
    return Pet(
        id=pet_id,
        external_id=external_id,
        type=pet_type,
        source=source,
        photos=[f"https://example.com/{pet_id}.jpg"],
        gender=PetGender.MALE,
        size=PetSize.MEDIUM,
        age=PetAge.YOUNG,
        good_with_children=True,
    )


def test_returns_local_results_immediately_when_limit_is_filled() -> None:
    pet_repository = Mock(spec=PetRepository)
    external_provider = Mock(spec=ExternalDogProvider)
    service = PetSearchService(pet_repository, external_provider)
    filters = PetSearchFilters(types=(PetType.DOG,))
    local_pets = [make_pet("local-1"), make_pet("local-2")]
    pet_repository.search.return_value = local_pets

    result = service.search(filters, limit=2)

    assert result == local_pets
    external_provider.search.assert_not_called()


def test_uses_external_provider_when_local_results_are_not_enough() -> None:
    pet_repository = Mock(spec=PetRepository)
    external_provider = Mock(spec=ExternalDogProvider)
    service = PetSearchService(pet_repository, external_provider)
    filters = PetSearchFilters(types=(PetType.DOG,))
    local_pet = make_pet("local-1")
    external_pet = make_pet(
        "external_dog_10",
        source=PetSource.EXTERNAL,
        external_id="10",
    )

    pet_repository.search.return_value = [local_pet]
    external_provider.search.return_value = [external_pet]

    result = service.search(filters, limit=2)

    assert result == [local_pet, external_pet]
    external_provider.search.assert_called_once_with(filters=filters.for_external_dogs(), limit=1)


def test_handles_mixed_type_filters_with_local_first_order() -> None:
    pet_repository = Mock(spec=PetRepository)
    external_provider = Mock(spec=ExternalDogProvider)
    service = PetSearchService(pet_repository, external_provider)
    filters = PetSearchFilters(types=(PetType.CAT, PetType.DOG), sizes=(PetSize.SMALL,))

    local_cat = make_pet("local-cat-1", pet_type=PetType.CAT)
    external_dog = make_pet(
        "external_dog_11",
        pet_type=PetType.DOG,
        source=PetSource.EXTERNAL,
        external_id="11",
    )

    pet_repository.search.return_value = [local_cat]
    external_provider.search.return_value = [external_dog]

    result = service.search(filters, limit=3)

    assert result == [local_cat, external_dog]
    external_provider.search.assert_called_once_with(
        filters=filters.for_external_dogs(),
        limit=2,
    )


def test_returns_empty_list_when_both_sources_have_no_results() -> None:
    pet_repository = Mock(spec=PetRepository)
    external_provider = Mock(spec=ExternalDogProvider)
    service = PetSearchService(pet_repository, external_provider)
    filters = PetSearchFilters(types=(PetType.DOG,))

    pet_repository.search.return_value = []
    external_provider.search.return_value = []

    result = service.search(filters, limit=5)

    assert result == []


def test_skips_external_lookup_for_non_dog_filters() -> None:
    pet_repository = Mock(spec=PetRepository)
    external_provider = Mock(spec=ExternalDogProvider)
    service = PetSearchService(pet_repository, external_provider)
    filters = PetSearchFilters(types=(PetType.CAT,))
    pet_repository.search.return_value = []

    result = service.search(filters, limit=3)

    assert result == []
    external_provider.search.assert_not_called()
