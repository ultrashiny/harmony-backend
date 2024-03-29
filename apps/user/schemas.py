from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserAuth(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=5, max_length=30, example="john123")
    password: str = Field(..., min_length=8, max_length=30)
    
class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: bool = False
    credits: int = 0

class ProfileSave(BaseModel):
    id: UUID
    name: str
    race: str
    points: list[list]