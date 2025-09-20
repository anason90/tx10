"""Business logic for project operations."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas

_PROJECT_TRANSITIONS = {
    models.ProjectStatus.PLANNING: {models.ProjectStatus.APPROVED},
    models.ProjectStatus.APPROVED: {models.ProjectStatus.CONSTRUCTION},
    models.ProjectStatus.CONSTRUCTION: {models.ProjectStatus.SALES},
    models.ProjectStatus.SALES: {models.ProjectStatus.COMPLETED},
    models.ProjectStatus.COMPLETED: set(),
}


def create_project(session: Session, payload: schemas.ProjectCreate) -> models.Project:
    project = models.Project(**payload.model_dump())
    session.add(project)
    session.flush()
    return project


def get_project(session: Session, project_id: int) -> models.Project | None:
    return session.get(models.Project, project_id)


def list_projects(session: Session) -> list[models.Project]:
    return session.scalars(select(models.Project)).all()


def update_project(session: Session, project: models.Project, payload: schemas.ProjectUpdate) -> models.Project:
    data = payload.model_dump(exclude_unset=True)
    next_status = data.get("status")
    if next_status is not None and next_status != project.status:
        allowed = _PROJECT_TRANSITIONS.get(project.status, set())
        if next_status not in allowed:
            raise ValueError(
                f"Cannot transition project {project.id} from {project.status} to {next_status}"
            )
    for key, value in data.items():
        setattr(project, key, value)
    session.flush()
    return project
