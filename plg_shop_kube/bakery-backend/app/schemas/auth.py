from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterInput(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=150)
    password: str = Field(min_length=12, max_length=128)

class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class RefreshInput(BaseModel):
    refresh_token: str = Field(min_length=20, max_length=200)

class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool

class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    user: UserOutput
