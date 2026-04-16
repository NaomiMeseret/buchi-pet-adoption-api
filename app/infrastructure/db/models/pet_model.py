from sqlalchemy import Boolean, Column, JSON, String, Text
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(String(64), primary_key=True)
    type = Column(String(32), nullable=False, index=True)
    source = Column(String(32), nullable=False, index=True)
    photos = Column(JSON, nullable=False, default=list)
    external_id = Column(String(128), nullable=True, index=True)
    name = Column(String(255), nullable=True)
    gender = Column(String(32), nullable=True, index=True)
    size = Column(String(32), nullable=True, index=True)
    age = Column(String(32), nullable=True, index=True)
    good_with_children = Column(Boolean, nullable=True, index=True)
    breed = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)

    adoption_requests = relationship("AdoptionRequestModel", back_populates="pet")
