from datetime import datetime
from uuid import UUID  # , uuid4

from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Uuid,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from APICore.result_models.cms.contents import CMSContent, CMSContentBase, CMSContents
from SQL_Connection.db_connection import Base, NotFoundError, SessionLocal
from SQL_Connection.tables.cms.tbl_cms_categories import create_new_category
from SQL_Connection.tables.cms.tbl_cms_contentAttachments import create_new_attachment
from SQL_Connection.tables.cms.tbl_cms_contentDownloads import create_new_download
from SQL_Connection.tables.cms.tbl_cms_contentFiles import create_new_file
from SQL_Connection.tables.cms.tbl_cms_contentLibraries import (
    create_new_content_library,
)
from SQL_Connection.tables.cms.tbl_cms_contentLoads import create_new_content_load
from SQL_Connection.tables.cms.tbl_cms_contentReviews import create_new_review
from SQL_Connection.tables.cms.tbl_cms_contentRevisions import create_new_revision
from SQL_Connection.tables.cms.tbl_cms_contentTags import create_new_content_tag


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblCMSContents(Base):
    __tablename__ = "contents"
    __table_args__ = {"schema": "cms"}

    id: Mapped[UUID] = mapped_column(
        Uuid(), primary_key=True, index=True, nullable=False
    )
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedById: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("accounts.users.id"),
        nullable=False,
    )
    updatedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updatedById: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("accounts.users.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    fileName: Mapped[str] = mapped_column(String(150), nullable=False)
    fileExtension: Mapped[str] = mapped_column(String(13), nullable=False)
    hasCustomPreviewImage: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    location: Mapped[str] = mapped_column(String(20), nullable=False)
    averageRating: Mapped[float] = mapped_column(Float(), nullable=False)
    categoryId: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("cms.categories.id"),
        nullable=True,
    )
    previewImageUri: Mapped[str] = mapped_column(String(2048), nullable=True)
    displayUnit: Mapped[str] = mapped_column(String(15), nullable=True)
    revitFamilyHostType: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")
    refreshedId: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("core.refreshed.id"),
        nullable=False,
    )


## function to write a new entry item in the table
def write_db_content(
    item: CMSContent,
    refreshed,
    session: Session = None,
) -> CMSContent:
    base_content = CMSContentBase(**item.model_dump())
    db_item = TblCMSContents(
        **base_content.model_dump(exclude_none=True),
        categoryId=item.category.id,
        refreshedId=refreshed.id,
    )
    if session is None:
        db = SessionLocal()
    else:
        db = session
    try:
        db_item = read_db_content(item, db)
    except NotFoundError:
        if item.category != []:
            create_new_category(item.category, refreshed)
        db.add(db_item)
        if item.category != []:
            create_new_category(item.category, refreshed)
        db.commit()
        db.refresh(db_item)
        if item.contentAttachments != []:
            [create_new_attachment(i, refreshed) for i in item.contentAttachments]
        if item.downloads != []:
            [create_new_download(i, refreshed) for i in item.downloads]
        if item.contentLibraries != []:
            [create_new_content_library(i, refreshed) for i in item.contentLibraries]
        if item.contentTags != []:
            [create_new_content_tag(i, refreshed) for i in item.contentTags]
        if item.loads != []:
            [create_new_content_load(i, refreshed, db) for i in item.loads]
        if item.reviews != []:
            [create_new_review(i, refreshed) for i in item.reviews]
        if item.revisions != []:
            [create_new_revision(i, refreshed) for i in item.revisions]
        if item.files != []:
            [create_new_file(i, refreshed) for i in item.files]
    if session is None:
        db.close()
    return CMSContent(**db_item.__dict__)


## function to read from the table
def get_all_contents(session: Session) -> CMSContents:
    if session is None:
        db = SessionLocal()
    else:
        db = session
    contents = CMSContents(totalItems=0, items=[])
    try:
        db_items = db.query(TblCMSContents).all()
        for db_item in db_items:
            contents.items.append(CMSContent(**db_item.__dict__))
        contents.totalItems = len(contents.items)
    except NotFoundError:
        raise NotFoundError("No content records found")
    finally:
        if session is None:
            db.close()
    return contents


## function to read from the table
def read_db_content(item: CMSContent, session: Session) -> CMSContent:
    if session is None:
        db = SessionLocal()
    else:
        db = session
    db_item = db.query(TblCMSContents).filter(TblCMSContents.id == item.id).first()
    if db_item is None:
        raise NotFoundError(f"ContentId: {item.id} not found")
    if session is None:
        db.close()
    return CMSContent(**db_item.__dict__)


## function to delete from the table
def delete_db_content():
    pass
