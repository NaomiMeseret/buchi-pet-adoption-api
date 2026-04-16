from dataclasses import dataclass
from datetime import datetime


@dataclass
class AdoptionRequest:
    id: str
    customer_id: str
    pet_id: str
    created_at: datetime
