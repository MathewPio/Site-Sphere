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