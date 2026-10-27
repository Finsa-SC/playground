from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator
class PostCreate(BaseModel):
    content: str | None = Field(default=None, max_length=5000)
    visibility: str = "public"
    @model_validator(mode="after")
    def validate_visibility(self):
        if self.visibility not in {"public", "followers"}:
            raise ValueError("visibility must be public or followers")
        if self.content is not None and not self.content.strip():
            raise ValueError("content cannot be blank")
        return self
class PostUpdate(BaseModel):
    content: str | None = Field(default=None, max_length=5000)
    visibility: str | None = None
    @model_validator(mode="after")
    def validate_fields(self):
        if self.visibility is not None and self.visibility not in {"public", "followers"}:
            raise ValueError("visibility must be public or followers")
        if self.content is not None and not self.content.strip():
            raise ValueError("content cannot be blank")
        return self
class MediaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    media_type: str
    media_url: str
    alt_text: str | None
    mime_type: str | None
    file_size_bytes: int | None
    width: int | None
    height: int | None
    position: int
class PostOut(BaseModel):
    id: UUID
    author_id: UUID
    content: str | None
    visibility: str
    created_at: datetime
    updated_at: datetime
    edited_at: datetime | None
    like_count: int = 0
    comment_count: int = 0
    liked_by_me: bool = False
    media: list[MediaOut] = Field(default_factory=list)
