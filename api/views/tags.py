from fastapi import APIRouter, HTTPException, status

from api.dependencies import (
    CurrentUserDep,
    PaginationDep,
    TagDataCreateDep,
    TagServiceDep,
)
import schemas

tags = APIRouter(prefix="/api/tags", tags=["Tags"])


@tags.get("", response_model=list[schemas.TagWithRelations])
async def get_tags(pagination: PaginationDep, tag_service: TagServiceDep):
    return await tag_service.get_all(pagination)


@tags.get("/{tag_id}", response_model=schemas.Tag)
async def get_tag(tag_id: int, tag_service: TagServiceDep):
    tag = await tag_service.get_by_id(tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@tags.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(
    data: TagDataCreateDep,
    current_user: CurrentUserDep,
    tag_service: TagServiceDep,
):
    data = schemas.TagCreateExtended(name=data.name, author_id=current_user.id)
    return await tag_service.add_one(data)


@tags.delete("/{tag_id}")
async def delete_tag(tag_id: int, tag_service: TagServiceDep):
    return await tag_service.delete(tag_id)
