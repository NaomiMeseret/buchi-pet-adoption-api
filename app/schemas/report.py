from datetime import date
from typing import Literal

from pydantic import BaseModel


class GenerateReportRequest(BaseModel):
    from_date: date
    to_date: date


class GenerateReportData(BaseModel):
    adopted_pet_types: dict[str, int]
    weekly_adoption_requests: dict[str, int]


class GenerateReportResponse(BaseModel):
    status: Literal["success"] = "success"
    data: GenerateReportData
