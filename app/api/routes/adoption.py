from datetime import date

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_adoption_service
from app.application.services import AdoptionService
from app.core.exceptions import BadRequestError
from app.domain.value_objects.date_range import DateRange
from app.schemas.adoption_request import (
    AdoptionRequestItemResponse,
    AdoptRequest,
    AdoptResponse,
    AdoptResponseData,
    GetAdoptionRequestsQuery,
    GetAdoptionRequestsResponse,
)


router = APIRouter(tags=["adoption"])


@router.post("/adopt", response_model=AdoptResponse)
def adopt(
    request: AdoptRequest,
    service: AdoptionService = Depends(get_adoption_service),
) -> AdoptResponse:
    adoption_request = service.create(
        customer_id=request.customer_id,
        pet_id=request.pet_id,
    )
    return AdoptResponse(
        data=AdoptResponseData(adoption_id=adoption_request.id),
    )


@router.get("/get_adoption_requests", response_model=GetAdoptionRequestsResponse)
def get_adoption_requests(
    from_date: date = Query(...),
    to_date: date = Query(...),
    service: AdoptionService = Depends(get_adoption_service),
) -> GetAdoptionRequestsResponse:
    query = GetAdoptionRequestsQuery(from_date=from_date, to_date=to_date)
    if query.from_date > query.to_date:
        raise BadRequestError("from_date cannot be after to_date")

    data = service.get_by_date_range(
        DateRange(start_date=query.from_date, end_date=query.to_date),
    )
    return GetAdoptionRequestsResponse(
        data=[
            AdoptionRequestItemResponse(
                customer_id=item["customer_id"],
                customer_phone=item["customer_phone"],
                customer_name=item["customer_name"],
                pet_id=item["pet_id"],
                type=item["type"].value.capitalize(),
                gender=item["gender"].value if item["gender"] else None,
                size=item["size"].value if item["size"] else None,
                age=item["age"].value if item["age"] else None,
                good_with_children=item["good_with_children"],
            )
            for item in data
        ]
    )
