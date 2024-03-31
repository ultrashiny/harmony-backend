from uuid import UUID
from pydantic import BaseModel

class ProfileSave(BaseModel):
    id: UUID
    name: str
    gender: int
    race: int
    points: list[list]