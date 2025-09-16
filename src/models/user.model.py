from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password_hash: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
