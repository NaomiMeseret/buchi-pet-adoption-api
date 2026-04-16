from fastapi import APIRouter, Depends

from app.api.deps import get_report_service
from app.application.services import ReportService
from app.core.exceptions import BadRequestError
from app.domain.value_objects.date_range import DateRange
from app.schemas.report import GenerateReportRequest, GenerateReportResponse


router = APIRouter(tags=["reports"])


@router.post("/generate_report", response_model=GenerateReportResponse)
def generate_report(
    request: GenerateReportRequest,
    service: ReportService = Depends(get_report_service),
) -> GenerateReportResponse:
    if request.from_date > request.to_date:
        raise BadRequestError("from_date cannot be after to_date")

    report = service.generate(
        DateRange(start_date=request.from_date, end_date=request.to_date),
    )
    return GenerateReportResponse(data=report)
