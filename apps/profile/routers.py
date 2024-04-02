from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from .service import ProfileService
from apps.user.deps import get_current_user
from apps.user.models import User
from .schemas import ProfileDownload, ProfileSave
import pymongo

profile_router = APIRouter()

@profile_router.post('/', summary="Save/Update one profile")
async def create_profile(data: ProfileSave, 
                        #  user: User = Depends(get_current_user)
                        ):
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return await ProfileService.save(data)

@profile_router.get('/{user_id}', summary="Get all profiles of current user")
async def get_profiles(user_id: UUID):
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return await ProfileService.get(user_id)

@profile_router.post('/download', summary="Download one profile")
async def download_profile(data: ProfileDownload):
    return await ProfileService.download(data)