from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserAuth(BaseModel):
    """User authentication model."""
    username: str
    email: EmailStr
    password: str


class UserRegister(UserAuth):
    """User registration model."""
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""
    username: str
    password: str


class UserResponse(BaseModel):
    """User response model without sensitive data."""
    id: str
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer" 