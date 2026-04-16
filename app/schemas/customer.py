from typing import Literal

from pydantic import BaseModel


class AddCustomerRequest(BaseModel):
    name: str
    phone: str


class AddCustomerResponseData(BaseModel):
    customer_id: str


class AddCustomerResponse(BaseModel):
    status: Literal["success"] = "success"
    data: AddCustomerResponseData
