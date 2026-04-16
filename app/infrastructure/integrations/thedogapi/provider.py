import re
from collections.abc import Sequence

from app.domain.entities.pet import Pet
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_source import PetSource
from app.domain.enums.pet_type import PetType
from app.domain.interfaces.external_dog_provider import ExternalDogProvider
from app.domain.value_objects.pet_search_filters import PetSearchFilters
from app.infrastructure.integrations.thedogapi.client import TheDogApiClient


class TheDogApiExternalDogProvider(ExternalDogProvider):
    def __init__(self, client: TheDogApiClient) -> None:
        self.client = client

    def search(self, filters: PetSearchFilters, limit: int) -> list[Pet]:
        if limit <= 0:
            return []

        requested_limit = limit
        if filters.sizes:
            requested_limit = min(limit * 3, 100)

        image_payloads = self.client.search_images(limit=requested_limit)
        pets: list[Pet] = []

        for image_payload in image_payloads:
            pet = self._to_domain_pet(image_payload)
            if pet is None:
                continue

            if not self._matches_filters(pet, filters):
                continue

            pets.append(pet)
            if len(pets) == limit:
                break

        return pets

    def get_by_id(self, pet_id: str) -> Pet | None:
        external_id = self._extract_external_id(pet_id)
        if external_id is None:
            return None

        image_payload = self.client.get_image_by_id(external_id)
        if image_payload is None:
            return None

        return self._to_domain_pet(image_payload)

    def _to_domain_pet(self, image_payload: dict) -> Pet | None:
        external_id = image_payload.get("id")
        if external_id is None:
            return None

        external_id = str(external_id)
        breed_payload = self._first_breed(image_payload.get("breeds"))
        breed_name = breed_payload.get("name")
        description = breed_payload.get("description") or breed_payload.get("temperament")
        size = self._infer_size(breed_payload)

        photo_url = image_payload.get("url")
        photos = [photo_url] if isinstance(photo_url, str) and photo_url else []

        return Pet(
            id=f"external_dog_{external_id}",
            external_id=external_id,
            type=PetType.DOG,
            source=PetSource.EXTERNAL,
            photos=photos,
            name=breed_name,
            size=size,
            breed=breed_name,
            description=description if isinstance(description, str) else None,
        )

    @staticmethod
    def _matches_filters(pet: Pet, filters: PetSearchFilters) -> bool:
        if filters.types and pet.type not in filters.types:
            return False

        if filters.sizes and pet.size not in filters.sizes:
            return False

        return True

    @staticmethod
    def _first_breed(breeds: object) -> dict:
        if not isinstance(breeds, Sequence) or not breeds:
            return {}

        first_breed = breeds[0]
        if not isinstance(first_breed, dict):
            return {}

        return first_breed

    def _infer_size(self, breed_payload: dict) -> PetSize | None:
        weights = []

        for field_name in (
            "male_weight_kg",
            "female_weight_kg",
        ):
            field_value = breed_payload.get(field_name)
            if isinstance(field_value, str):
                weights.extend(self._extract_numbers(field_value))

        weight_payload = breed_payload.get("weight")
        if isinstance(weight_payload, dict):
            metric_weight = weight_payload.get("metric")
            if isinstance(metric_weight, str):
                weights.extend(self._extract_numbers(metric_weight))

        if not weights:
            return None

        average_weight = sum(weights) / len(weights)

        if average_weight <= 10:
            return PetSize.SMALL
        if average_weight <= 25:
            return PetSize.MEDIUM
        if average_weight <= 40:
            return PetSize.LARGE
        return PetSize.XLARGE

    @staticmethod
    def _extract_numbers(value: str) -> list[float]:
        matches = re.findall(r"\d+(?:\.\d+)?", value)
        return [float(match) for match in matches]

    @staticmethod
    def _extract_external_id(pet_id: str) -> str | None:
        prefix = "external_dog_"
        if not pet_id.startswith(prefix):
            return None

        external_id = pet_id.removeprefix(prefix)
        return external_id or None
