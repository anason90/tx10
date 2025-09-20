"""Business logic for units and ownership."""
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas

_UNIT_TRANSITIONS = {
    models.UnitStatus.DESIGN: {models.UnitStatus.AVAILABLE},
    models.UnitStatus.AVAILABLE: {models.UnitStatus.RESERVED, models.UnitStatus.SOLD},
    models.UnitStatus.RESERVED: {models.UnitStatus.SOLD, models.UnitStatus.AVAILABLE},
    models.UnitStatus.SOLD: {models.UnitStatus.TRANSFERRED},
    models.UnitStatus.TRANSFERRED: set(),
}


def create_unit(session: Session, payload: schemas.UnitCreate) -> models.Unit:
    unit = models.Unit(**payload.model_dump())
    session.add(unit)
    session.flush()
    return unit


def list_units(session: Session) -> list[models.Unit]:
    return session.scalars(select(models.Unit)).all()


def update_unit(session: Session, unit: models.Unit, payload: schemas.UnitUpdate) -> models.Unit:
    data = payload.model_dump(exclude_unset=True)
    desired_status = data.get("status")
    if desired_status is not None and desired_status != unit.status:
        _validate_transition(unit.status, desired_status)
    for key, value in data.items():
        setattr(unit, key, value)
    session.flush()
    return unit


def bulk_transition(session: Session, units: Iterable[models.Unit], next_status: models.UnitStatus) -> None:
    for unit in units:
        _validate_transition(unit.status, next_status)
        unit.status = next_status
    session.flush()


def set_unit_shares(
    session: Session, unit: models.Unit, shares: list[schemas.UnitShareCreate]
) -> list[models.UnitShare]:
    unit.shares.clear()
    total = 0.0
    for share in shares:
        total += share.share_percentage
        unit.shares.append(models.UnitShare(**share.model_dump()))
    if total > 100.0 + 1e-6:
        raise ValueError("Total share percentage cannot exceed 100")
    session.flush()
    return unit.shares


def _validate_transition(current: models.UnitStatus, desired: models.UnitStatus) -> None:
    allowed = _UNIT_TRANSITIONS.get(current, set())
    if desired not in allowed:
        raise ValueError(f"Invalid transition from {current} to {desired}")
