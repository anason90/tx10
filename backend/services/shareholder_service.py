"""Business logic for shareholder management."""
from sqlalchemy.orm import Session

from .. import models, schemas


def create_shareholder(
    session: Session, payload: schemas.ShareholderCreate
) -> models.Shareholder:
    shareholder = models.Shareholder(**payload.model_dump())
    session.add(shareholder)
    session.flush()
    return shareholder


def list_shareholders(session: Session) -> list[models.Shareholder]:
    return session.query(models.Shareholder).all()
