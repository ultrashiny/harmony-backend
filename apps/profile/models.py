from typing import List
from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field

class Profile(Document):
    profile_id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
    name: str = Indexed(str)
    gender: int = Indexed(int)
    race: int = Indexed(int)
    points: list[list]

    def __repr__(self) -> str:
        return f"<Profile profile_id={self.profile_id}>"
    
    def __str__(self) -> str:
        return self.name
    
    @classmethod
    async def by_user_id(cls, user_id:UUID) -> List['Profile']:
        return await cls.find(cls.user_id == user_id).to_list()

    class Settings:
        name = "profiles"