from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, Session, mapped_column

from APICore.result_models.cms.content_attachments import CMSContentAttachment
from SQL_Connection.db_connection import Base, NotFoundError, SessionLocal


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblCMSContentAttachments(Base):
    __tablename__ = "contentAttachments"
    __table_args__ = {"schema": "cms"}

    id: Mapped[uuid4] = mapped_column(
        Uuid(), primary_key=True, index=True, nullable=False
    )
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedById: Mapped[uuid4] = mapped_column(
        ForeignKey("accounts.users.id"), nullable=False
    )
    updatedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updatedById: Mapped[uuid4] = mapped_column(
        ForeignKey("accounts.users.id"), nullable=False
    )
    fileExtension: Mapped[str] = mapped_column(String(10), nullable=True)
    fileSizeinBytes: Mapped[int] = mapped_column(Integer(), nullable=True)
    contentId: Mapped[uuid4] = mapped_column(
        ForeignKey("cms.contents.id"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
    isLink: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    name: Mapped[str] = mapped_column(String(2048), nullable=False)
    path: Mapped[str] = mapped_column(String(2048), nullable=False)
    type: Mapped[int] = mapped_column(String(100), nullable=False)
    refreshedId: Mapped[uuid4] = mapped_column(
        ForeignKey("core.refreshed.id"), nullable=False
    )


## function to write to create a new entry item in the table
def create_new_attachment(
    item: CMSContentAttachment, refreshed
) -> CMSContentAttachment:
    base_attachment = CMSContentAttachment(**item.model_dump())
    base_attachment.refreshedId = refreshed.id
    new_entry = TblCMSContentAttachments(
        **base_attachment.model_dump(exclude_none=True)
    )
    db = SessionLocal()
    try:
        new_entry = read_db_attachment(item, db)
    except NotFoundError:
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
    finally:
        db.close()
    return new_entry


## function to read from the table
def read_db_attachment(
    item: CMSContentAttachment, session: Session
) -> CMSContentAttachment:
    db_attachment = (
        session.query(TblCMSContentAttachments)
        .filter(TblCMSContentAttachments.id == item.id)
        .first()
    )
    if db_attachment is None:
        raise NotFoundError(f"AttachmentId: {item.id} not found")
    return db_attachment


## function to update the table
def update_entry():
    pass


## function to delete from the table
def delete_entry():
    pass
