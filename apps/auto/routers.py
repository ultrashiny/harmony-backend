import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from apps.user.deps import get_current_user
from apps.user.models import User
from .service import ImageService
from .schemas import FeaturePoints
from .f_service import mainProcess as f_mainProcess
from .s_service import mainProcess as s_mainProcess

auto_router = APIRouter()

@auto_router.post('/f/{id}', summary="Detect points for front profile", response_model=FeaturePoints)
async def front_mapping(id: str, 
                        # user: User = Depends(get_current_user)
                        ):
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return f_mainProcess(id)


@auto_router.post('/s/{id}', summary="Detect points for side profile", response_model=FeaturePoints)
async def side_mapping(id: str,
                        # user: User = Depends(get_current_user)
                        ):
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return s_mainProcess(id)