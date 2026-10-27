from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, AliasChoices


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=50)
    bio: str | None = Field(default=None, max_length=280)
    website_url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=100)


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    display_name: str
    bio: str | None
    avatar_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("avatar_url", "avatar_key"),
    )
    banner_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("banner_url", "banner_key"),
    )
    website_url: str | None
    location: str | None