from fastapi import APIRouter, Depends, HTTPException, status

from apps.user.deps import get_current_user
from apps.user.models import User
from .schemas import FeaturePoints
from .service import FeatureService

feat_router = APIRouter()

@feat_router.post('/', summary="Calculate measurement values")
async def calculate(data: FeaturePoints, user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return await FeatureService.calculate(data)
