from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.api.deps import get_create_pet_service, get_pet_search_service
from app.application.services import CreatePetService, PetPhotoInput, PetSearchService
from app.core.exceptions import BadRequestError
from app.domain.enums.pet_age import PetAge
from app.domain.enums.pet_gender import PetGender
from app.domain.enums.pet_size import PetSize
from app.domain.enums.pet_type import PetType
from app.schemas.pet import (
    CreatePetRequest,
    CreatePetResponse,
    CreatePetResponseData,
    GetPetsQuery,
    GetPetsResponse,
    GetPetsResponseData,
    PetItemResponse,
)


router = APIRouter(tags=["pets"])


async def parse_create_pet_request(
    type: PetType = Form(...),
    gender: PetGender = Form(...),
    size: PetSize = Form(...),
    age: PetAge = Form(...),
    good_with_children: bool = Form(...),
    photos: list[UploadFile] = File(...),
) -> tuple[CreatePetRequest, list[UploadFile]]:
    if not photos:
        raise BadRequestError("at least one photo is required")

    return (
        CreatePetRequest(
            type=type,
            gender=gender,
            size=size,
            age=age,
            good_with_children=good_with_children,
        ),
        photos,
    )


@router.post("/create_pet", response_model=CreatePetResponse)
async def create_pet(
    payload: Annotated[tuple[CreatePetRequest, list[UploadFile]], Depends(parse_create_pet_request)],
    service: CreatePetService = Depends(get_create_pet_service),
) -> CreatePetResponse:
    request_data, upload_files = payload
    photos = [
        PetPhotoInput(filename=file.filename or "photo.jpg", content=await file.read())
        for file in upload_files
    ]

    pet = service.create(
        pet_type=request_data.type,
        gender=request_data.gender,
        size=request_data.size,
        age=request_data.age,
        good_with_children=request_data.good_with_children,
        photos=photos,
    )

    return CreatePetResponse(
        data=CreatePetResponseData(pet_id=pet.id),
    )


@router.get("/get_pets", response_model=GetPetsResponse)
def get_pets(
    type: Annotated[list[PetType] | None, Query()] = None,
    gender: Annotated[list[PetGender] | None, Query()] = None,
    size: Annotated[list[PetSize] | None, Query()] = None,
    age: Annotated[list[PetAge] | None, Query()] = None,
    good_with_children: bool | None = Query(default=None),
    limit: int = Query(..., gt=0),
    service: PetSearchService = Depends(get_pet_search_service),
) -> GetPetsResponse:
    query = GetPetsQuery(
        types=type or [],
        genders=gender or [],
        sizes=size or [],
        ages=age or [],
        good_with_children=good_with_children,
        limit=limit,
    )
    pets = service.search(query.to_filters(), query.limit)
    return GetPetsResponse(
        data=GetPetsResponseData(
            pets=[PetItemResponse.from_domain(pet) for pet in pets],
        )
    )
