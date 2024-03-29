from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class Profile(BaseModel):
    gender: int = 0
    racial: int = 0
    feature:  dict = {}

class Report(BaseModel):
    indexes: dict = {}