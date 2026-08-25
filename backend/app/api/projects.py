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
from app.schemas.project import (
    ProjectCreate, 
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project import (
    create_project,
    get_projects,
    get_project_by_id,
    update_project,
    delete_project,
)

from app.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberResponse,
    ProjectMemberDetailResponse,
)

from app.services.project_member import (
    add_project_member,
    get_project_members,
    remove_project_member,
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


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = update_project(
        db=db,
        project_id=project_id,
        organization_id=current_user.organization_id,
        project_data=project_data,
    )
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
        
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_project(
        db=db,
        project_id=project_id,
        organization_id=current_user.organization_id,   
    )
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
        
    return None



@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member_to_project(
    member_data: ProjectMemberCreate,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # The service performs the important security checks:
    # - project belongs to current organisation
    # - user belongs to current organisation
    # - user isn't already assigned to the project
    
    project_member, error = add_project_member(
        db=db,
        project_id=project_id,
        user_id=member_data.user_id,
        organization_id=current_user.organization_id,
    )
    
    # convert service errors into apprioprate HTTP responses.
    if error == "project_not_found":
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if error == "user_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in you organization"
        )
        
    if error == "already_member":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this project",
        )
        
    return project_member


@router.get(
    "/{project_id}/members",
    response_model=list[ProjectMemberDetailResponse],
)
def get_members_of_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only retrieve members if the project belongs
    # to the authenticated user's organisation.
    members = get_project_members(
        project_id = project_id,
        db=db,
        organization_id=current_user.organization_id,
    )
    
    if members is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return members



@router.delete(
    "/{project_id}/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member_from_project(
    project_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted, error = remove_project_member(
        db=db,
        project_id=project_id,
        member_id=member_id,
        organization_id=current_user.organization_id
    )
    
    if error == "project_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
        
    if error == "member_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project member not found",
        )
        
    return None