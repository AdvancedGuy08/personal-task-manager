from fastapi import APIRouter, HTTPException, status

from api.dependencies import (
    CurrentUserDep,
    PaginationDep,
    ProjectDataCreateDep,
    ProjectServiceDep,
)
import schemas


projects = APIRouter(prefix="/api/projects", tags=["Projects"])


@projects.get("", response_model=list[schemas.ProjectWithRelations])
async def get_projects(pagination: PaginationDep, project_service: ProjectServiceDep):
    return await project_service.get_all(pagination)


@projects.get("/{project_id}", response_model=schemas.Project)
async def get_project(project_id: int, project_service: ProjectServiceDep):
    project = await project_service.get_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


@projects.post("", status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectDataCreateDep,
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
):
    data = schemas.ProjectCreateExtended(name=data.name, owner_id=current_user.id)
    return await project_service.add_one(data)


@projects.delete("/{project_id}")
async def delete_project(project_id: int, project_service: ProjectServiceDep):
    return await project_service.delete(project_id)


@projects.patch("/{project_id}")
async def update_project(
    project_id: int, data: schemas.ProjectUpdate, project_service: ProjectServiceDep
):
    return await project_service.update(project_id, data)
