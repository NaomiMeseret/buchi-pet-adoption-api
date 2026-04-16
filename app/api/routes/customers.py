from fastapi import APIRouter, Depends

from app.api.deps import get_customer_service
from app.application.services import CustomerService
from app.schemas.customer import AddCustomerRequest, AddCustomerResponse, AddCustomerResponseData


router = APIRouter(tags=["customers"])


@router.post("/add_customer", response_model=AddCustomerResponse)
def add_customer(
    request: AddCustomerRequest,
    service: CustomerService = Depends(get_customer_service),
) -> AddCustomerResponse:
    customer = service.create_or_get(name=request.name, phone=request.phone)
    return AddCustomerResponse(
        data=AddCustomerResponseData(customer_id=customer.id),
    )
