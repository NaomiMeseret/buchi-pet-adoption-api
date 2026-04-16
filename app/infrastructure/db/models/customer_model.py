from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(32), nullable=False, unique=True, index=True)

    adoption_requests = relationship("AdoptionRequestModel", back_populates="customer")
