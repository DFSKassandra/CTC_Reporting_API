from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, Session, mapped_column

from APICore.result_models.accounts.groups import AccGroup, AccGroupBase
from SQL_Connection.db_connection import Base, NotFoundError, SessionLocal
from SQL_Connection.tables.accounts.tbl_acc_groupMembers import create_new_group_member
from SQL_Connection.tables.accounts.tbl_acc_groupRoles import create_new_group_role


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblAccGroups(Base):
    __tablename__ = "groups"
    __table_args__ = {"schema": "accounts"}

    id: Mapped[uuid4] = mapped_column(
        Uuid(), primary_key=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedById: Mapped[uuid4] = mapped_column(
        ForeignKey("accounts.users.id"), nullable=False
    )
    updatedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updatedById: Mapped[uuid4] = mapped_column(
        ForeignKey("accounts.users.id"), nullable=False
    )
    isDefaultGroup: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    refreshedId: Mapped[uuid4] = mapped_column(
        ForeignKey("core.refreshed.id"), nullable=False
    )


## function to write to create a new entry item in the table
def create_new_group(item: AccGroup, refreshed) -> AccGroup:
    base_item = AccGroupBase(**item.model_dump(exclude_none=True))
    new_entry = TblAccGroups(
        **base_item.model_dump(exclude_none=True), refreshedId=refreshed.id
    )
    db = SessionLocal()
    try:
        new_entry = read_db_group(item, db)
    except NotFoundError:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        if item.roleAssignments != []:
            [create_new_group_role(role, refreshed, db) for role in item.groupRoles]
        if item.groupMembers != []:
            [
                create_new_group_member(member, refreshed, db)
                for member in item.groupMembers
            ]
    finally:
        db.close()
    return new_entry


## function to read item from the table
def read_db_group(item: AccGroup, session: Session) -> AccGroup:
    db_item = session.query(TblAccGroups).filter(TblAccGroups.id == item.id).first()
    if db_item is None:
        raise NotFoundError(f"GroupId: {item.id} not found")
    db_item_dump = {}
    for key, value in db_item.__dict__.items():
        db_item_dump.update({key: value})
    return AccGroup(**db_item_dump)


## function to update the table
def update_group(item: AccGroup, session: Session) -> AccGroup:
    update_entry = read_db_group(item, session)
    if item.updatedAt.astimezone(None) > update_entry.updatedAt.astimezone(None):
        for key, value in item.model_dump().items():
            if key != "id":
                setattr(update_entry, key, value)
    session.commit()
    session.refresh(update_entry)
    return update_entry


## function to delete from the table
def delete_entry():
    pass
