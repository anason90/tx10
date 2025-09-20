"""Sales assignment endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import sales_service
from .deps import get_db

router = APIRouter(prefix="/sales", tags=["sales"])


def _get_assignment(db: Session, assignment_id: int) -> models.SalesAssignment:
    assignment = db.get(models.SalesAssignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.post(
    "/representatives",
    response_model=schemas.SalesRepresentativeRead,
    status_code=status.HTTP_201_CREATED,
)
def register_sales_rep(
    payload: schemas.SalesRepresentativeCreate, db: Session = Depends(get_db)
) -> schemas.SalesRepresentativeRead:
    rep = sales_service.register_sales_rep(db, payload)
    return schemas.SalesRepresentativeRead.model_validate(rep)


@router.post(
    "/assignments",
    response_model=schemas.AssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
def assign_sales_rep(
    payload: schemas.AssignmentCreate, db: Session = Depends(get_db)
) -> schemas.AssignmentRead:
    assignment = sales_service.assign_sales_rep(db, payload)
    return schemas.AssignmentRead.model_validate(assignment)


@router.get("/assignments", response_model=list[schemas.AssignmentRead])
def list_assignments(db: Session = Depends(get_db)) -> list[schemas.AssignmentRead]:
    assignments = sales_service.list_assignments(db)
    return [schemas.AssignmentRead.model_validate(item) for item in assignments]


@router.patch("/assignments/{assignment_id}", response_model=schemas.AssignmentRead)
def update_assignment_status(
    assignment_id: int,
    payload: schemas.AssignmentStatusUpdate,
    db: Session = Depends(get_db),
) -> schemas.AssignmentRead:
    assignment = _get_assignment(db, assignment_id)
    assignment = sales_service.update_assignment_status(db, assignment, payload.status)
    return schemas.AssignmentRead.model_validate(assignment)
