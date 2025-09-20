"""Project endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..services import project_service
from .deps import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: schemas.ProjectCreate, db: Session = Depends(get_db)
) -> schemas.ProjectRead:
    project = project_service.create_project(db, payload)
    return schemas.ProjectRead.model_validate(project)


@router.get("/", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)) -> list[schemas.ProjectRead]:
    projects = project_service.list_projects(db)
    return [schemas.ProjectRead.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> schemas.ProjectRead:
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return schemas.ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)
) -> schemas.ProjectRead:
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        project = project_service.update_project(db, project, payload)
    except ValueError as exc:  # invalid transition
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return schemas.ProjectRead.model_validate(project)
