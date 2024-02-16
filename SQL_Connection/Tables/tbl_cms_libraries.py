from sqlalchemy import DateTime, Uuid, String, Boolean, Float, Integer, ForeignKey
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from SQL_Connection.db_connection import Base
from pydantic import BaseModel
from typing import Optional


## creating the pydantic BaseModel
class CMS_Libraries(BaseModel):
    id: UUID
    addedAt: datetime
    addedById: UUID
    updatedAt: datetime
    updatedById: UUID
    name: str
    type: str
    description: str
    uploadContent: bool
    defaultRole: str
    imageUri: str
    refreshedId: UUID


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class Tbl_CMS_Libraries(Base):
    __tablename__ = 'libraries'
    __table_args__ = {"schema": "cms"}

    id: Mapped[uuid4] = mapped_column(Uuid(), primary_key=True, index=True, nullable=False)
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedById: Mapped[uuid4] = mapped_column(ForeignKey('accounts.users.id'), nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updatedById: Mapped[uuid4] = mapped_column(ForeignKey('accounts.users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(15), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
    uploadContent: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    defaultRole: Mapped[str] = mapped_column(String(15), nullable=False)
    imageUri: Mapped[str] = mapped_column(String(2048), nullable=True)
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
