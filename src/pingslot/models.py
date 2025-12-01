from __future__ import annotations

from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship  # type: ignore
from sqlalchemy import UniqueConstraint



class Platform(str, Enum):
    TELEGRAM = "telegram"
    QQ = "qq"


class BookingStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    invite_code: str
    resources: list[Resource] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}, cascade_delete=True
    )
    bookings: list[Booking] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}, cascade_delete=True
    )
    user_bindings: list[UserBinding] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}, cascade_delete=True
    )


class UserBinding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    platform: Platform
    platform_user_id: str

    __table_args__ = (
        UniqueConstraint("platform", "platform_user_id", name="uix_platform_user"),
    )



class Resource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str = Field(unique=True)
    description: str | None = None


class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    resource_id: int = Field(foreign_key="resource.id", ondelete="CASCADE")
    status: BookingStatus = Field(default=BookingStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="bookings")
    resource: Resource = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
