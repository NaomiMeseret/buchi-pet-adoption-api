from abc import ABC, abstractmethod

from app.domain.entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Create and return a customer."""

    @abstractmethod
    def get_by_id(self, customer_id: str) -> Customer | None:
        """Return one customer by id or None when it does not exist."""

    @abstractmethod
    def get_by_phone(self, phone_number: str) -> Customer | None:
        """Return one customer by phone number or None when it does not exist."""

    @abstractmethod
    def phone_exists(self, phone_number: str) -> bool:
        """Return True when the phone number is already used."""
