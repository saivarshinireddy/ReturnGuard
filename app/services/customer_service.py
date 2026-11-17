
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
    existing_customer = db.scalar(
        select(Customer).where(Customer.email == customer_data.email)
    )

    if existing_customer:
        raise ValueError("A customer with this email already exists")

    customer = Customer(
        name=customer_data.name,
        email=str(customer_data.email),
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


def get_customers(db: Session) -> list[Customer]:
    return list(db.scalars(select(Customer).order_by(Customer.id)).all())
