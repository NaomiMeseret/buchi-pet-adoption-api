from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.entities.adoption_request import AdoptionRequest
from app.domain.enums.adoption_request_status import AdoptionRequestStatus
from app.domain.interfaces.adoption_repository import AdoptionRepository
from app.domain.value_objects.date_range import DateRange
from app.infrastructure.db.models.adoption_request_model import AdoptionRequestModel


class AdoptionRepositorySQLAlchemy(AdoptionRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_date_range(self, date_range: DateRange) -> list[AdoptionRequest]:
        statement = (
            select(AdoptionRequestModel)
            .where(func.date(AdoptionRequestModel.created_at) >= date_range.start_date)
            .where(func.date(AdoptionRequestModel.created_at) <= date_range.end_date)
            .order_by(AdoptionRequestModel.created_at.asc())
        )
        adoption_request_models = self.session.scalars(statement).all()
        return [self._to_domain(model) for model in adoption_request_models]

    def create(self, adoption_request: AdoptionRequest) -> AdoptionRequest:
        adoption_request_model = self._to_model(adoption_request)
        self.session.add(adoption_request_model)
        self.session.commit()
        self.session.refresh(adoption_request_model)
        return self._to_domain(adoption_request_model)

    @staticmethod
    def _to_domain(adoption_request_model: AdoptionRequestModel) -> AdoptionRequest:
        return AdoptionRequest(
            id=adoption_request_model.id,
            customer_id=adoption_request_model.customer_id,
            pet_id=adoption_request_model.pet_id,
            created_at=adoption_request_model.created_at,
            status=AdoptionRequestStatus(adoption_request_model.status),
        )

    @staticmethod
    def _to_model(adoption_request: AdoptionRequest) -> AdoptionRequestModel:
        return AdoptionRequestModel(
            id=adoption_request.id,
            customer_id=adoption_request.customer_id,
            pet_id=adoption_request.pet_id,
            created_at=adoption_request.created_at,
            status=adoption_request.status.value,
        )
