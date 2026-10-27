from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    parent_comment_id: UUID | None = None
class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    post_id: UUID
    author_id: UUID
    parent_comment_id: UUID | None
    content: str
    created_at: datetime
    updated_at: datetime
