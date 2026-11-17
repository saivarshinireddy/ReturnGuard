
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order
from app.schemas.order import OrderCreate


def create_order(db: Session, order_data: OrderCreate) -> Order:
    customer = db.get(Customer, order_data.customer_id)

    if customer is None:
        raise ValueError("Customer does not exist")

    order = Order(
        customer_id=order_data.customer_id,
        product_name=order_data.product_name,
        amount=order_data.amount,
        status="delivered",
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_order(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)


def get_orders(db: Session) -> list[Order]:
    return list(db.scalars(select(Order).order_by(Order.id)).all())
