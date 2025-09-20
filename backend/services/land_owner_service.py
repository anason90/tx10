"""Business logic for land owners."""
from sqlalchemy.orm import Session

from .. import models, schemas


def create_land_owner(session: Session, payload: schemas.LandOwnerCreate) -> models.LandOwner:
    land_owner = models.LandOwner(**payload.model_dump())
    session.add(land_owner)
    session.flush()
    return land_owner


def list_land_owners(session: Session) -> list[models.LandOwner]:
    return session.query(models.LandOwner).all()
