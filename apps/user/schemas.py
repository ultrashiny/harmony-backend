from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserAuth(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=3, max_length=30, example="leo")
    password: str = Field(..., min_length=8, max_length=30)
    
class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: bool = False
    credit: int = 0
    
class UserSubscription(BaseModel):
    user_id: UUID
    customer_id: str
    payment_method_id: str
    price_id: str
    
class UserUpdate(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    customer_id: str
    subscription_id: str
    first_name: str
    last_name: str
    credit: int
    auth: int
    
class UserPayload(BaseModel):
    event: str
    data: dict