"""module that defines the result models for CMS Content"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from APICore.api_get_functions import get_all_x, get_total_items, get_x_by_id
from APICore.connection_models.collections import content, contents
from APICore.connection_models.scopes import cms
from APICore.result_models.cms.content_attachments import CMSContentAttachment
from APICore.result_models.cms.content_categories import CMSCategory
from APICore.result_models.cms.content_downloads import CMSContentDownload
from APICore.result_models.cms.content_favorited_users import CMSContentFavoritedUser
from APICore.result_models.cms.content_files import CMSContentFile
from APICore.result_models.cms.content_loads import CMSContentLoad
from APICore.result_models.cms.content_reviews import CMSContentReview
from APICore.result_models.cms.content_revisions import CMSContentRevision


## creating the pydantic BaseModel
class CMSContentBase(BaseModel):
    id: UUID
    addedAt: datetime
    addedById: UUID
    updatedAt: datetime
    updatedById: UUID
    name: str
    fileName: str
    fileExtension: str
    hasCustomPreviewImage: bool
    type: str
    source: str
    location: str
    averageRating: float
    categoryId: Optional[int] | None = None
    previewImageUri: Optional[str] | None = None
    displayUnit: Optional[str] | None = None
    revitFamilyHostType: Optional[str] | None = None
    refreshedId: Optional[UUID] | None = None


class CMSContent(CMSContentBase):
    category: Optional[CMSCategory] = []
    files: Optional[List[CMSContentFile]] = []
    contentAttachments: Optional[List[CMSContentAttachment]] = []
    downlaods: Optional[List[CMSContentDownload]] = []
    loads: Optional[List[CMSContentLoad]] = []
    reviews: Optional[List[CMSContentReview]] = []
    revisions: Optional[List[CMSContentRevision]] = []
    contentTagIds: Optional[List[UUID]] = []
    contentLibraryIds: Optional[List[UUID]] = []
    favoritedUsers: Optional[List[CMSContentFavoritedUser]] = []


class CMSContents(BaseModel):
    totalItems: int
    items: Optional[List[CMSContent]] = []


## base function(s) for use with this model
def get_all_content() -> CMSContents:
    total_items = get_total_items(scope=cms, collection=contents)
    result = get_all_x(scope=cms, collection=contents, total_rows=total_items)
    return CMSContents.model_validate(result)


def get_content_details_by_id(*, item: CMSContent) -> CMSContent:
    result = get_x_by_id(scope=cms, collection=content, item_id=item.id)
    return CMSContent.model_validate(result)


def get_all_content_details(objects: CMSContents) -> CMSContents:
    new_objects = CMSContents(totalItems=0, items=[])
    for item in objects.items:
        new_item = get_content_details_by_id(item=item)
        new_objects.items.append(new_item)
        new_objects.totalItems = len(new_objects.items)
    return new_objects
