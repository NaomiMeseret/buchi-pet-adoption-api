from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.entities.customer import Customer
from app.domain.interfaces.customer_repository import CustomerRepository
from app.infrastructure.db.models.customer_model import CustomerModel


class CustomerRepositorySQLAlchemy(CustomerRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_phone(self, phone: str) -> Customer | None:
        statement = select(CustomerModel).where(CustomerModel.phone == phone)
        customer_model = self.session.scalar(statement)
        if customer_model is None:
            return None

        return self._to_domain(customer_model)

    def get_by_id(self, customer_id: str) -> Customer | None:
        statement = select(CustomerModel).where(CustomerModel.id == customer_id)
        customer_model = self.session.scalar(statement)
        if customer_model is None:
            return None

        return self._to_domain(customer_model)

    def create(self, customer: Customer) -> Customer:
        customer_model = self._to_model(customer)
        self.session.add(customer_model)

        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError("customer phone already exists") from exc

        self.session.refresh(customer_model)
        return self._to_domain(customer_model)

    @staticmethod
    def _to_domain(customer_model: CustomerModel) -> Customer:
        return Customer(
            id=customer_model.id,
            name=customer_model.name,
            phone=customer_model.phone,
        )

    @staticmethod
    def _to_model(customer: Customer) -> CustomerModel:
        return CustomerModel(
            id=customer.id,
            name=customer.name,
            phone=customer.phone,
        )
