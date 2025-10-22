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


class Project(ProjectCreate):
    id: int


class ProjectWithOwner(Project):
    owner: "User"


class UserCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str
    email: EmailStr


class UserMeta(Timestamp):
    is_active: bool


class User(UserCreate, UserMeta):
    id: int


class UserWithProjects(User):
    projects: list[Project]
