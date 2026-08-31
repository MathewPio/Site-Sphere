from app.models.project import Project
from sqlalchemy.orm import Session
from app.schemas.project_update import (
    ProjectUpdateCreate,
    ProjectUpdateUpdate,
    ProjectUpdateResponse,
)
from app.models.project_member import ProjectMember
from app.models.project_update import ProjectUpdate

def create_project_update(
    db: Session,
    project_id: int,
    organization_id: int,
    user_id: int,
    update_data: ProjectUpdateCreate,
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.organization_id == organization_id,
        )
        .first()
    )
    
    if not project:
        return None, "project_not_found"
    
    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )
    
    if not member:
        return None, "user_not_project_member"
    
    project_update = ProjectUpdate(
        project_id=project_id,
        user_id=user_id,
        **update_data.model_dump(),
    )
    
    db.add(project_update)
    db.commit()
    db.refresh(project_update)
    
    return project_update, None



def get_project_updates(
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
    
    if not project:
        return None, "project_not_found"
    
    
    project_updates = (
        db.query(ProjectUpdate)
        .filter(
            ProjectUpdate.project_id == project_id
        )
        .order_by(ProjectUpdate.created_at.desc())
        .all()
    )
    
    return project_updates, None
    