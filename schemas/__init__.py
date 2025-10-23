from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class Timestamp(BaseModel):
    created_at: datetime
    updated_at: datetime


class Pagination(BaseModel):
    limit: int = Field(default=10, ge=0, le=100)
    offset: int = Field(default=0, ge=0)


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=128)


class ProjectCreateExtended(ProjectCreate):
    owner_id: int


class Project(ProjectCreateExtended, Timestamp):
    id: int


class ProjectWithRelations(Project):
    owner: "User"
    tags: list["Tag"]


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=128)
    tags: list["Tag"] | None = None


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)
    color: str = Field(..., min_length=6, max_length=6)


class TagCreateExtended(TagCreate):
    author_id: int


class Tag(TagCreateExtended):
    id: int


class TagWithRelations(Tag):
    author: "User"
    projects: list["Project"]


class UserCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str
    email: EmailStr


class UserMeta(Timestamp):
    is_active: bool


class User(UserCreate, UserMeta):
    id: int


class UserWithRelations(User):
    projects: list["Project"]
    authored_tags: list["Tag"]
