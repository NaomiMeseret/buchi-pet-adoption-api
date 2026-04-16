"""initial schema

Revision ID: 20260416_01
Revises:
Create Date: 2026-04-16 15:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260416_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_phone"), "customers", ["phone"], unique=True)

    op.create_table(
        "pets",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("photos", sa.JSON(), nullable=False),
        sa.Column("external_id", sa.String(length=128), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("gender", sa.String(length=32), nullable=True),
        sa.Column("size", sa.String(length=32), nullable=True),
        sa.Column("age", sa.String(length=32), nullable=True),
        sa.Column("good_with_children", sa.Boolean(), nullable=True),
        sa.Column("breed", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pets_age"), "pets", ["age"], unique=False)
    op.create_index(op.f("ix_pets_external_id"), "pets", ["external_id"], unique=False)
    op.create_index(op.f("ix_pets_gender"), "pets", ["gender"], unique=False)
    op.create_index(op.f("ix_pets_good_with_children"), "pets", ["good_with_children"], unique=False)
    op.create_index(op.f("ix_pets_size"), "pets", ["size"], unique=False)
    op.create_index(op.f("ix_pets_source"), "pets", ["source"], unique=False)
    op.create_index(op.f("ix_pets_type"), "pets", ["type"], unique=False)

    op.create_table(
        "adoption_requests",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("customer_id", sa.String(length=64), nullable=False),
        sa.Column("pet_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["pet_id"], ["pets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_adoption_requests_created_at"), "adoption_requests", ["created_at"], unique=False)
    op.create_index(op.f("ix_adoption_requests_customer_id"), "adoption_requests", ["customer_id"], unique=False)
    op.create_index(op.f("ix_adoption_requests_pet_id"), "adoption_requests", ["pet_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_adoption_requests_pet_id"), table_name="adoption_requests")
    op.drop_index(op.f("ix_adoption_requests_customer_id"), table_name="adoption_requests")
    op.drop_index(op.f("ix_adoption_requests_created_at"), table_name="adoption_requests")
    op.drop_table("adoption_requests")

    op.drop_index(op.f("ix_pets_type"), table_name="pets")
    op.drop_index(op.f("ix_pets_source"), table_name="pets")
    op.drop_index(op.f("ix_pets_size"), table_name="pets")
    op.drop_index(op.f("ix_pets_good_with_children"), table_name="pets")
    op.drop_index(op.f("ix_pets_gender"), table_name="pets")
    op.drop_index(op.f("ix_pets_external_id"), table_name="pets")
    op.drop_index(op.f("ix_pets_age"), table_name="pets")
    op.drop_table("pets")

    op.drop_index(op.f("ix_customers_phone"), table_name="customers")
    op.drop_table("customers")
