"""Module that defines the result models for CMS ContentReviews"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


## creating the pydantic BaseModel
class CMSContentReview(BaseModel):
    id: UUID
    contentId: UUID
    rating: int
    comment: Optional[str] | None = None
    addedAt: datetime
    addedById: UUID
    updatedAt: datetime
    updatedById: UUID
    refreshedId: Optional[UUID] | None = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, CMSContentReview):
            return NotImplemented
        return (
            self.id == other.id
            and self.updatedAt == other.updatedAt
            and self.contentId == other.contentId
        )
