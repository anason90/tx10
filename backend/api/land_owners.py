"""Land owner endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas
from ..services import land_owner_service
from .deps import get_db

router = APIRouter(prefix="/land-owners", tags=["land owners"])


@router.post("/", response_model=schemas.LandOwnerRead, status_code=status.HTTP_201_CREATED)
def create_land_owner(
    payload: schemas.LandOwnerCreate, db: Session = Depends(get_db)
) -> schemas.LandOwnerRead:
    owner = land_owner_service.create_land_owner(db, payload)
    return schemas.LandOwnerRead.model_validate(owner)


@router.get("/", response_model=list[schemas.LandOwnerRead])
def list_land_owners(db: Session = Depends(get_db)) -> list[schemas.LandOwnerRead]:
    owners = land_owner_service.list_land_owners(db)
    return [schemas.LandOwnerRead.model_validate(owner) for owner in owners]
