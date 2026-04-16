from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base


class AdoptionRequestModel(Base):
    __tablename__ = "adoption_requests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    customer_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )
    pet_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("pets.id"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")

    customer: Mapped["CustomerModel"] = relationship(back_populates="adoption_requests")
    pet: Mapped["PetModel"] = relationship(back_populates="adoption_requests")
