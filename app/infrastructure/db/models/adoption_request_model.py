from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class AdoptionRequestModel(Base):
    __tablename__ = "adoption_requests"

    id = Column(String(64), primary_key=True)
    customer_id = Column(String(64), ForeignKey("customers.id"), nullable=False, index=True)
    pet_id = Column(String(64), ForeignKey("pets.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(String(32), nullable=False, default="pending")

    customer = relationship("CustomerModel", back_populates="adoption_requests")
    pet = relationship("PetModel", back_populates="adoption_requests")
