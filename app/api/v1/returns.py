
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.return_request import (
    ReturnRequestCreate,
    ReturnRequestResponse,
)
from app.services import return_service

router = APIRouter(prefix="/returns", tags=["Returns"])


@router.post(
    "",
    response_model=ReturnRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_return(
    request_data: ReturnRequestCreate,
    db: Session = Depends(get_db),
):
    try:
        return return_service.create_return_request(db, request_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[ReturnRequestResponse])
def list_returns(db: Session = Depends(get_db)):
    return return_service.get_return_requests(db)


@router.get("/{request_id}", response_model=ReturnRequestResponse)
def retrieve_return(
    request_id: int,
    db: Session = Depends(get_db),
):
    return_request = return_service.get_return_request(db, request_id)

    if return_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Return request not found",
        )

    return return_request
