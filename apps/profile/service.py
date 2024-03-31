from uuid import UUID

from apps.user.deps import get_current_user
from apps.user.models import User
from .schemas import ProfileSave
from apps.security import get_password, verify_password
from typing import List, Optional
from .models import Profile

class ProfileService:
    @staticmethod
    async def save(data: ProfileSave, user: User):
        existing_profile = await Profile.find_one(Profile.profile_id == data.id)
        if existing_profile:
            await existing_profile.update(
                {
                    "$set": {
                        "user_id": user.user_id,
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
                user_id=user.user_id,
                name = data.name,
                gender = data.gender,
                race=data.race,
                points=data.points
            )
            await profile_in.save()
            return profile_in
        
    async def get(user: User) -> List[Profile]:
        profiles = await Profile.by_user_id(user.user_id)
        return profiles