from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import (
    create_project,
    get_projects,
    get_project_by_id
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = create_project(
        db=db,
        project_data=project_data,
        organization_id=current_user.organization_id,
    )
    
    return project



@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_all_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    projects = get_projects(
        db=db,
        organization_id=current_user.organization_id,
    )
    
    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_single_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(
        db=db,
        project_id=project_id,
        organization_id=current_user.organization_id
    )
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project