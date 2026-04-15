from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    id: str
    full_name: str
    phone_number: str
    email: str | None = None
    address: str | None = None
    created_at: datetime | None = None
