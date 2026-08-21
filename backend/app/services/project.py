from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def create_project(
    db: Session,
    project_data: ProjectCreate,
    organization_id: int,
):
    project = Project(
        organization_id = organization_id,
        **project_data.model_dump()
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project


def get_projects(
    db: Session,
    organization_id: int,
):
    projects = (
        db.query(Project)
        .filter(
            Project.organization_id == organization_id
        )
        .all()
    )
    
    return projects


def get_project_by_id(
    db: Session,
    project_id: int,
    organization_id: int,
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == organization_id,
        )
        .first()
    )
    
    return project