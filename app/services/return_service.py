
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.return_request import ReturnRequest
from app.schemas.return_request import ReturnRequestCreate


def create_return_request(
    db: Session,
    request_data: ReturnRequestCreate,
) -> ReturnRequest:

    order = db.get(Order, request_data.order_id)

    if order is None:
        raise ValueError("Order does not exist")

    if order.status != "delivered":
        raise ValueError("Only delivered orders can be returned")

    existing_request = db.scalar(
        select(ReturnRequest).where(
            ReturnRequest.order_id == request_data.order_id,
            ReturnRequest.status.in_(["pending", "approved"]),
        )
    )

    if existing_request:
        raise ValueError("An active return request already exists")

    return_request = ReturnRequest(
        order_id=request_data.order_id,
        reason=request_data.reason,
        status="pending",
    )

    db.add(return_request)
    db.commit()
    db.refresh(return_request)

    return return_request


def get_return_request(
    db: Session,
    request_id: int,
) -> ReturnRequest | None:

    return db.get(ReturnRequest, request_id)


def get_return_requests(db: Session) -> list[ReturnRequest]:

    statement = select(ReturnRequest).order_by(ReturnRequest.id)

    return list(db.scalars(statement).all())
