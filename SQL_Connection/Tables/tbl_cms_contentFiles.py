from sqlalchemy import DateTime, Uuid, String, Boolean, Float, Integer, ForeignKey
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from SQL_Connection.db_connection import Base
from pydantic import BaseModel
from typing import Optional

## creating the pydantic BaseModel
class CMS_ContentFiles(BaseModel):
    id: UUID
    addedAt: datetime
    addedById: UUID
    updatedAt: datetime
    updatedById: UUID
    fileName: str
    filePath: str
    fileExtension: str
    fileSizeinBytes: int
    fileCreatedAt: datetime
    fileModifiedAt: datetime
    fileVersion: int
    contentId: UUID
    hasRevitTypeCatalog: bool
    revitSourceProjectElementId: int
    revitContainerProjectElementId: int
    revitProjectWorksharingMode: int
    location: str
    refreshedId: UUID

## Using SQLAlchemy2.0 generate Table with association to the correct schema
class Tbl_CMS_ContentFiles(Base):
    __tablename__ = 'contentFiles'
    __table_args__ = {"schema": "cms"}

    id: Mapped[uuid4] = mapped_column(Uuid(), primary_key=True, index=True, nullable=False)
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedById: Mapped[uuid4] = mapped_column(ForeignKey('accounts.users.id'), nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updatedById: Mapped[uuid4] = mapped_column(ForeignKey('accounts.users.id'), nullable=False)
    fileName: Mapped[str] = mapped_column(String(150), nullable=False)
    filePath: Mapped[str] = mapped_column(String(255), nullable=False)
    fileExtension: Mapped[str] = mapped_column(String(13), nullable=False)
    fileSizeinBytes: Mapped[int] = mapped_column(Integer(), nullable=False)
    fileCreatedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    fileModifiedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    fileVersion: Mapped[int] = mapped_column(Integer(), nullable=False)
    contentId: Mapped[uuid4] = mapped_column(ForeignKey('cms.contents.id'), nullable=False)
    hasRevitTypeCatalog: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    revitSourceProjectElementId: Mapped[int] = mapped_column(Integer(), nullable=False)
    revitContainerProjectElementId: Mapped[int] = mapped_column(Integer(), nullable=False)
    revitProjectWorksharingMode: Mapped[int] = mapped_column(Integer(), nullable=False)
    location: Mapped[str] = mapped_column(String(25), nullable=False)
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