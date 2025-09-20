"""Shareholder endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas
from ..services import shareholder_service
from .deps import get_db

router = APIRouter(prefix="/shareholders", tags=["shareholders"])


@router.post("/", response_model=schemas.ShareholderRead, status_code=status.HTTP_201_CREATED)
def create_shareholder(
    payload: schemas.ShareholderCreate, db: Session = Depends(get_db)
) -> schemas.ShareholderRead:
    shareholder = shareholder_service.create_shareholder(db, payload)
    return schemas.ShareholderRead.model_validate(shareholder)


@router.get("/", response_model=list[schemas.ShareholderRead])
def list_shareholders(db: Session = Depends(get_db)) -> list[schemas.ShareholderRead]:
    shareholders = shareholder_service.list_shareholders(db)
    return [schemas.ShareholderRead.model_validate(item) for item in shareholders]
