from abc import ABC, abstractmethod

from app.domain.entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def get_by_phone(self, phone: str) -> Customer | None:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: str) -> Customer | None:
        pass

    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        pass
