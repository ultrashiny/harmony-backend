import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from apps.user.deps import get_current_user
from apps.user.models import User
from .service import ImageService

img_router = APIRouter()

@img_router.post('/{id}/{direction}', summary="Upload one image")
async def upload(id: str, direction: str, img: UploadFile = File(...), user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    dir = Path(f"./UPLOADS/{id}")
    dir.mkdir(parents=True, exist_ok=True)
    return await ImageService.save(dir, direction, img)

@img_router.post('/generate/{id}', summary="Generate feature images")
async def generate(id: str, points: str, lines: str, user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    dir = Path(f"./GENERATE/{id}")
    dir.mkdir(parents=True, exist_ok=True)
    return await ImageService.generate(id,json.JSONDecoder().decode(points), json.JSONDecoder().decode(lines))


@img_router.get('/feat/{id}/{index}', summary="Get one feature image")
async def get_feature_image(id: str, index: int):
    img_path = f"./GENERATES/{id}/{index}.jpg"
    return FileResponse(img_path, media_type="image/jpeg")

@img_router.get('/{id}/{direction}', summary="Get one profile image")
async def get_profile_image(id: str, direction: str):
    img_path = f"./UPLOADS/{id}/{direction}.jpg"
    return FileResponse(img_path, media_type="image/jpeg")