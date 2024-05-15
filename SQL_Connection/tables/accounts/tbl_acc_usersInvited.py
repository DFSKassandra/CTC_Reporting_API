from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, Session, mapped_column

from APICore.result_models.accounts.users_invited import AccInvitedUser
from SQL_Connection.db_connection import Base, NotFoundError, SessionLocal


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblAccUsersInvited(Base):
    __tablename__ = "usersInvited"
    __table_args__ = {"schema": "accounts"}

    userId: Mapped[uuid4] = mapped_column(
        Uuid(), primary_key=True, index=True, nullable=False
    )
    userName: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    idEnabled: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    invitationExpiration: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    refreshedId: Mapped[uuid4] = mapped_column(
        ForeignKey("core.refreshed.id"), nullable=False
    )


## function to write to create a new entry item in the table
def create_new_entry():
    pass


## function to read from the table
def read_db_user_invited(item: AccInvitedUser, session: Session) -> AccInvitedUser:
    db_item = (
        session.query(TblAccUsersInvited)
        .filter(TblAccUsersInvited.userId == item.userId)
        .first()
    )
    if db_item is None:
        raise NotFoundError(f"UserId: {item.userId} not found")
    db_item_dump = {}
    for key, value in db_item.__dict__.items():
        db_item_dump.update({key: value})
    return AccInvitedUser(**db_item_dump)


## function to update the table
def update_entry():
    pass


## function to delete from the table
def delete_entry():
    pass
