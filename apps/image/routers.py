import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from apps.user.deps import get_current_user
from apps.user.models import User
from .service import ImageService
from .schemas import ImageFeatures

img_router = APIRouter()

@img_router.post('/{id}/{direction}', summary="Upload one image")
async def upload(id: str, direction: str, img: UploadFile = File(...), 
                #  user: User = Depends(get_current_user)
                 ):
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    dir = Path(f"./UPLOADS/{id}")
    dir.mkdir(parents=True, exist_ok=True)
    return await ImageService.save(dir, direction, img)

@img_router.post('/generate', summary="Generate feature images")
async def generate(features: ImageFeatures, 
                #    user: User = Depends(get_current_user)
                   ):
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    dir = Path(f"./GENERATES/{features.id}")
    dir.mkdir(parents=True, exist_ok=True)
    return await ImageService.generate(features.id,features.points, features.lines)


@img_router.get('/feat/{id}/{index}', summary="Get one feature image")
async def get_feature_image(id: str, index: int):
    img_path = f"./GENERATES/{id}/{index}.jpg"
    return FileResponse(img_path, media_type="image/jpeg")

@img_router.get('/{id}/{direction}', summary="Get one profile image")
async def get_profile_image(id: str, direction: str):
    img_path = f"./UPLOADS/{id}/{direction}.jpg"
    path_obj = Path(img_path)
    if not path_obj.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You need to upload the images")
    
    return FileResponse(img_path, media_type="image/jpeg")