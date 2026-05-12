from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=255)


class CurrentUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str | None = None
    role: str
    is_active: bool


class LoginData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: CurrentUserRead


class LoginResponse(BaseModel):
    success: bool = True
    data: LoginData

