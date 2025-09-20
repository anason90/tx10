"""Unit endpoints covering lifecycle transitions."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import unit_service
from .deps import get_db

router = APIRouter(prefix="/units", tags=["units"])


def _get_unit_or_404(db: Session, unit_id: int) -> models.Unit:
    unit = db.get(models.Unit, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.post("/", response_model=schemas.UnitRead, status_code=status.HTTP_201_CREATED)
def create_unit(payload: schemas.UnitCreate, db: Session = Depends(get_db)) -> schemas.UnitRead:
    unit = unit_service.create_unit(db, payload)
    return schemas.UnitRead.model_validate(unit)


@router.get("/", response_model=list[schemas.UnitRead])
def list_units(db: Session = Depends(get_db)) -> list[schemas.UnitRead]:
    units = unit_service.list_units(db)
    return [schemas.UnitRead.model_validate(unit) for unit in units]


@router.patch("/{unit_id}", response_model=schemas.UnitRead)
def update_unit(
    unit_id: int, payload: schemas.UnitUpdate, db: Session = Depends(get_db)
) -> schemas.UnitRead:
    unit = _get_unit_or_404(db, unit_id)
    try:
        unit = unit_service.update_unit(db, unit, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return schemas.UnitRead.model_validate(unit)


@router.post("/{unit_id}/transition", response_model=schemas.UnitRead)
def transition_unit(
    unit_id: int, payload: schemas.UnitStatusTransition, db: Session = Depends(get_db)
) -> schemas.UnitRead:
    unit = _get_unit_or_404(db, unit_id)
    try:
        unit = unit_service.update_unit(
            db, unit, schemas.UnitUpdate(status=payload.next_status)
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return schemas.UnitRead.model_validate(unit)


@router.post("/bulk-transition", response_model=list[schemas.UnitRead])
def bulk_transition(
    payload: schemas.BulkUnitStatusUpdate, db: Session = Depends(get_db)
) -> list[schemas.UnitRead]:
    units = [
        _get_unit_or_404(db, unit_id)
        for unit_id in payload.unit_ids
    ]
    try:
        unit_service.bulk_transition(db, units, payload.next_status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return [schemas.UnitRead.model_validate(unit) for unit in units]


@router.put("/{unit_id}/shares", response_model=list[schemas.UnitShareRead])
def update_unit_shares(
    unit_id: int, shares: list[schemas.UnitShareCreate], db: Session = Depends(get_db)
) -> list[schemas.UnitShareRead]:
    unit = _get_unit_or_404(db, unit_id)
    try:
        updated_shares = unit_service.set_unit_shares(db, unit, shares)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return [schemas.UnitShareRead.model_validate(share) for share in updated_shares]
