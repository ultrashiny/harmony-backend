from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class ImageFeatures(BaseModel):
    id: str
    points: list[list]
    lines: list[list]