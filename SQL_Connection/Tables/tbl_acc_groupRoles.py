from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from SQL_Connection.db_connection import Base


## creating the pydantic BaseModel
class AccGroupRole(BaseModel):
    groupId: UUID
    roleId: int
    refreshedId: Optional[UUID] = None


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblAccGroupRoles(Base):
    __tablename__ = "groupRoles"
    __table_args__ = {"schema": "accounts"}

    groupId: Mapped[uuid4] = mapped_column(
        Uuid(),
        ForeignKey("accounts.groups.id"),
        primary_key=True,
        index=True,
        nullable=False,
    )
    roleId: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("accounts.roles.id"),
        primary_key=True,
        index=True,
        nullable=False,
    )
    refreshedId: Mapped[uuid4] = mapped_column(
        ForeignKey("core.refreshed.id"), nullable=False
    )


## function to write to create a new entry item in the table
def create_new_entry():
    pass


## function to read from the table
def get_all_items():
    pass


## function to update the table
def update_entry():
    pass


## function to delete from the table
def delete_entry():
    pass
