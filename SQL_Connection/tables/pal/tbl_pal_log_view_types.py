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

from APICore.result_models.pal.doc_sessions import PALLogViewType
from SQL_Connection.db_connection import Base, NotFoundError, SessionLocal


## Using SQLAlchemy2.0 generate Table with association to the correct schema
class TblPALLogViewTypes(Base):
    __tablename__ = "logViewTypes"
    __table_args__ = {"schema": "pal"}

    id: Mapped[UUID] = mapped_column(
        Uuid(), primary_key=True, index=True, nullable=False
    )
    docSessionId: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("pal.docSessions.id"), nullable=False
    )
    viewTypeName: Mapped[str] = mapped_column(String(255), nullable=False)
    viewCt: Mapped[int] = mapped_column(Integer, nullable=False)
    logDate: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    addedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    uploadedAt: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    refreshedId: Mapped[UUID] = mapped_column(
        ForeignKey("core.refreshed.id"), nullable=False
    )


## function to write new entry item to the table
def write_db_log_view_type(
    item: PALLogViewType,
    refreshed,
    session: Session = None,
) -> PALLogViewType:
    base_item = item.model_dump(exclude_none=True)
    db_item = TblPALLogViewTypes(**base_item, refreshedId=refreshed.id)
    if session is None:
        db = SessionLocal()
    else:
        db = session
    try:
        read_db_log_view_type(item, db)
    except NotFoundError:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    if session is None:
        db.close()
    return PALLogViewType(**db_item.__dict__)


## function to read item from the table
def read_db_log_view_type(item: PALLogViewType, session: Session) -> PALLogViewType:
    db_item = (
        session.query(TblPALLogViewTypes)
        .filter(TblPALLogViewTypes.id == item.id)
        .first()
    )
    if db_item is None:
        raise NotFoundError(f"LogViewTypeId: {item.id} not found")
    return PALLogViewType(**db_item.__dict__)


## function to update the table
def update_log_view_type():
    pass


## function to delete item from the table
def delete_log_view_type():
    pass
