from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user model."""
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """User creation model with password."""
    password: str

class User(UserBase):
    """User response model."""
    id: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True 