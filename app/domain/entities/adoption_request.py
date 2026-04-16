from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.adoption_request_status import AdoptionRequestStatus


@dataclass
class AdoptionRequest:
    id: str
    customer_id: str
    pet_id: str
    created_at: datetime
    status: AdoptionRequestStatus = AdoptionRequestStatus.PENDING
