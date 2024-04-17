from uuid import UUID
from pydantic import BaseModel

class ProfileSave(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    gender: int
    race: int
    points: list[list]
    date: str

class ProfileDownload(BaseModel):
    id: UUID
    name: str = "Unnamed"
    gender: str = "Male"
    race: str = "Caucasian"
    features: list