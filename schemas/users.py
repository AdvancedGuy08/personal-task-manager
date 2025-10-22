from typing import Any
from pydantic import BaseModel, EmailStr

from .timestamp import Timestamp


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
    projects: list[Any]
