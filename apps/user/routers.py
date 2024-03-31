from fastapi import APIRouter, Depends, HTTPException, status

from apps.user.deps import get_current_user
from apps.user.models import User
from .schemas import UserAuth, UserOut
from .service import UserService
import pymongo

user_router = APIRouter()

@user_router.post('/create', summary="Create a new user", response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or email already exists."
        )