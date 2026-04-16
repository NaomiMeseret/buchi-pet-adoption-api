from datetime import date
from typing import Literal

from pydantic import BaseModel


class AdoptRequest(BaseModel):
    customer_id: str
    pet_id: str


class AdoptResponseData(BaseModel):
    adoption_id: str


class AdoptResponse(BaseModel):
    status: Literal["success"] = "success"
    data: AdoptResponseData


class GetAdoptionRequestsQuery(BaseModel):
    from_date: date
    to_date: date


class AdoptionRequestItemResponse(BaseModel):
    customer_id: str
    customer_phone: str
    customer_name: str
    pet_id: str
    type: str
    gender: str | None = None
    size: str | None = None
    age: str | None = None
    good_with_children: bool | None = None


class GetAdoptionRequestsResponse(BaseModel):
    status: Literal["success"] = "success"
    data: list[AdoptionRequestItemResponse]
