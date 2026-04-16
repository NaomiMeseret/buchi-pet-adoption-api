from uuid import uuid4

from app.core.exceptions import ConflictError
from app.domain.entities.customer import Customer
from app.domain.interfaces.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    def create_or_get(self, *, name: str, phone: str) -> Customer:
        existing_customer = self.customer_repository.get_by_phone(phone)
        if existing_customer is not None:
            return existing_customer

        customer = Customer(
            id=str(uuid4()),
            name=name,
            phone=phone,
        )

        try:
            return self.customer_repository.create(customer)
        except ValueError as exc:
            raise ConflictError(str(exc)) from exc
