from app.schemas.adoption_request import (
    AdoptionRequestItemResponse,
    AdoptRequest,
    AdoptResponse,
    GetAdoptionRequestsQuery,
    GetAdoptionRequestsResponse,
)
from app.schemas.common import ErrorResponse
from app.schemas.customer import AddCustomerRequest, AddCustomerResponse
from app.schemas.pet import (
    CreatePetRequest,
    CreatePetResponse,
    GetPetsQuery,
    GetPetsResponse,
    PetItemResponse,
)
from app.schemas.report import GenerateReportRequest, GenerateReportResponse

__all__ = [
    "ErrorResponse",
    "CreatePetRequest",
    "CreatePetResponse",
    "GetPetsQuery",
    "GetPetsResponse",
    "PetItemResponse",
    "AddCustomerRequest",
    "AddCustomerResponse",
    "AdoptRequest",
    "AdoptResponse",
    "AdoptionRequestItemResponse",
    "GetAdoptionRequestsQuery",
    "GetAdoptionRequestsResponse",
    "GenerateReportRequest",
    "GenerateReportResponse",
]
