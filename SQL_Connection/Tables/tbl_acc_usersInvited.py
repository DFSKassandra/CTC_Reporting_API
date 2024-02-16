from sqlalchemy import DateTime, Uuid, String, Boolean, ForeignKey
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from SQL_Connection.db_connection import Base
from pydantic import BaseModel


## creating the pydantic BaseModel
class Acc_UsersInvited(BaseModel):
    userId: UUID
    userName: str
    email: str
    idEnabled: bool
    invitationExpiration: datetime
    invitedLibraryPermissions: list[dict]
    refreshedId: UUID

## Using SQLAlchemy2.0 generate Table with association to the correct schema
class Tbl_Acc_UsersInvited(Base):
    __tablename__ = 'usersInvited'
    __table_args__ = {"schema": "accounts"}

    userId: Mapped[uuid4] = mapped_column(Uuid(), primary_key=True, index=True, nullable=False)
    userName: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    idEnabled: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    invitationExpiration: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    refreshedId: Mapped[uuid4] = mapped_column(ForeignKey('core.refreshed.id'), nullable=False)

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
