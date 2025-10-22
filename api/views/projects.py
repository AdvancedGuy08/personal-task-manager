from fastapi import APIRouter, HTTPException, status

from api.dependencies import (
    CurrentUserDep,
    PaginationDep,
    ProjectDataCreateDep,
    ProjectServiceDep,
)
import schemas


projects = APIRouter(prefix="/api/projects", tags=["Projects"])


@projects.get("", response_model=list[schemas.ProjectWithOwner])
async def get_projects(pagination: PaginationDep, user_service: ProjectServiceDep):
    return await user_service.get_all(pagination)


@projects.get("/{project_id}", response_model=schemas.Project)
async def get_project(project_id: int, user_service: ProjectServiceDep):
    project = await user_service.get_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return project


@projects.post("", status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectDataCreateDep,
    current_user: CurrentUserDep,
    user_service: ProjectServiceDep,
):
    data = schemas.ProjectCreateExtended(name=data.name, owner_id=current_user.id)
    return await user_service.add_one(data)


@projects.delete("/{project_id}")
async def delete_project(project_id: int, user_service: ProjectServiceDep):
    return await user_service.delete(project_id)
