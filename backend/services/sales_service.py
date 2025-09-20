"""Business logic related to sales assignments."""
from datetime import datetime

from sqlalchemy.orm import Session

from .. import models, schemas


def register_sales_rep(
    session: Session, payload: schemas.SalesRepresentativeCreate
) -> models.SalesRepresentative:
    rep = models.SalesRepresentative(**payload.model_dump())
    session.add(rep)
    session.flush()
    return rep


def assign_sales_rep(
    session: Session, payload: schemas.AssignmentCreate
) -> models.SalesAssignment:
    assignment = models.SalesAssignment(**payload.model_dump())
    session.add(assignment)
    session.flush()
    return assignment


def update_assignment_status(
    session: Session, assignment: models.SalesAssignment, status: models.AssignmentStatus
) -> models.SalesAssignment:
    assignment.status = status
    if status != models.AssignmentStatus.ACTIVE:
        assignment.assigned_at = assignment.assigned_at or datetime.utcnow()
    session.flush()
    return assignment


def list_assignments(session: Session) -> list[models.SalesAssignment]:
    return session.query(models.SalesAssignment).all()
