import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    projects: Mapped[list["Project"]] = relationship(back_populates="owner")
    authored_tags: Mapped[list["Tag"]] = relationship(back_populates="author")


project_tag = sa.Table(
    "projects_tags",
    Base.metadata,
    sa.Column("project_id", sa.ForeignKey("projects.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
)


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        sa.CheckConstraint("LENGTH(name) >= 3", name="ck_name_min_length"),
        sa.CheckConstraint("LENGTH(name) <= 128", name="ck_name_max_length"),
    )

    name: Mapped[str] = mapped_column(index=True)
    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="projects")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=project_tag, back_populates="projects"
    )


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        sa.CheckConstraint("LENGTH(name) > 0", name="ck_name_min_length"),
        sa.CheckConstraint("LENGTH(name) <= 32", name="ck_name_max_length"),
        sa.CheckConstraint("LENGTH(color) = 6", name="ck_name_strict_length"),
    )

    name: Mapped[str] = mapped_column(index=True, unique=True)
    color: Mapped[str]
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="authored_tags")
    projects: Mapped[list["Project"]] = relationship(
        secondary=project_tag, back_populates="tags"
    )
