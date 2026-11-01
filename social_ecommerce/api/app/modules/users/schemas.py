from pydantic import BaseModel, ConfigDict, Field


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    bio: str | None = Field(default=None, max_length=1000)


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    username: str
    display_name: str
    bio: str | None
    avatar_key: str | None
    banner_key: str | None
