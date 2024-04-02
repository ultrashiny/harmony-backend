from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field, EmailStr
from typing import Optional

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: str = Indexed(str, unique=True)
    email: EmailStr = Indexed(EmailStr, unique=True)
    hashed_password: str
    customer_id: Optional[str] = None
    subscription_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False
    credits: Optional[int] = 0
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def __str__(self) -> EmailStr:
        return self.email
    
    def __hash__(self) -> int:
        return hash(self.email)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, User):
            return self.email == __value.email
        return False
    
    @property
    def create(self):
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    
    class Settings:
        name = "users"
