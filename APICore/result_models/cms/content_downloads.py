"""Module that defines the result models for CMS ContentDownloads"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


## creating the pydantic BaseModel
class CMSContentDownload(BaseModel):
    id: UUID
    contentId: UUID
    downloadedAt: datetime
    downloadedById: UUID
    refreshedId: Optional[UUID] | None = None
