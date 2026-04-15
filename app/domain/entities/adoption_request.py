from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.adoption_request_status import AdoptionRequestStatus


@dataclass
class AdoptionRequest:
    id: str
    customer_id: str
    pet_id: str
    status: AdoptionRequestStatus = AdoptionRequestStatus.PENDING
    requested_at: datetime | None = None
    notes: str | None = None
