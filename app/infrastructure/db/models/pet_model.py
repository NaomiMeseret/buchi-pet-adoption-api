from __future__ import annotations

from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base


class PetModel(Base):
    __tablename__ = "pets"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    photos: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    external_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    size: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    age: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    good_with_children: Mapped[bool | None] = mapped_column(Boolean, nullable=True, index=True)
    breed: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    adoption_requests: Mapped[list["AdoptionRequestModel"]] = relationship(back_populates="pet")
