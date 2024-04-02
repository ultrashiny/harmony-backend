import os
from uuid import UUID

from fastapi.responses import FileResponse

from apps.user.deps import get_current_user
from apps.user.models import User
from .schemas import ProfileDownload, ProfileSave
from apps.security import get_password, verify_password
from typing import List, Optional
from .models import Profile
from .document import create_document

class ProfileService:
    @staticmethod
    async def save(data: ProfileSave):
        existing_profile = await Profile.find_one(Profile.profile_id == data.id)
        if existing_profile:
            await existing_profile.update(
                {
                    "$set": {
                        "user_id": data.user_id,
                        "name": data.name,
                        "gender": data.gender,
                        "race": data.race,
                        "points": data.points,
                    }
                }
            )
            return await Profile.find_one(Profile.profile_id == data.id)
        else:
            profile_in = Profile(
                profile_id=data.id,
                user_id=data.user_id,
                name = data.name,
                gender = data.gender,
                race=data.race,
                points=data.points
            )
            await profile_in.save()
            return profile_in
        
    async def get(user_id: str) -> List[Profile]:
        profiles = await Profile.by_user_id(user_id)
        return profiles
    
    async def download(data: ProfileDownload):
        DIR = f"./REPORTS"
        os.makedirs(DIR, exist_ok = True)   
        await create_document(f"{DIR}/{data.id}.xlsx", data)
        return FileResponse(f"{DIR}/{data.id}.xlsx")