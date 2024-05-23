import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
import httpx

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

@img_router.get('/mask/{id}', summary="Get one mask image")
async def get_mask_image(id: str):
    img_path = f"./UPLOADS/{id}/mask.jpg"
    path_obj = Path(img_path)
    # if not path_obj.exists():
    await ImageService.generate_mask(id)
    
    return FileResponse(img_path, media_type="image/jpeg")

@img_router.get('/canny/{id}', summary="Get one canny image")
async def get_canny_image(id: str):
    img_path = f"./UPLOADS/{id}/canny.jpg"
    path_obj = Path(img_path)
    # if not path_obj.exists():
    await ImageService.generate_canny(id)
        
    return FileResponse(img_path, media_type="image/jpeg")

@img_router.get('/ideal/{id}', summary="Get idealized faces")
async def get_idealize_image(id: str):
    url = "https://modelslab.com/api/v1/enterprise/controlnet"
    payload = json.dumps({
        "key": "u1rtaxxctmrwp1",
        "model_id": "realistic-vision-v51",
        "init_image": f"https://harmonyapp.ai/api/img/{id}/f",
        "mask_image": f"https://harmonyapp.ai/api/img/mask/{id}",
        "control_image": f"https://harmonyapp.ai/api/img/{id}/f",
        "width": "512",
        "height": "512",
        "prompt": "8K, HD, realistic raw photo, white, male, sexy, most handsome, most attractive, best quality skin, masterpiece, best quality, sharp focus, natural lighting, shadow, (((photorealistic))), octane render, HDR, 8k, high contrast , Canon EOS R3, nikon, f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical balance, in-frame, 8K, ((no make up))",
        "guess_mode": None,
        "use_karras_sigmas": None,
        "algorithm_type": None,
        "safety_checker_type": "no",
        "tomesd": "no",
        "vae": None,
        "embeddings": "epicrealism",
        "embeddings_model": "epicrealism",
        "upscale": None,
        "instant_response": None,
        "num_inference_steps": 31,
        "strength": 1,
        "negative_prompt": "",
        "guidance": "7.5",
        "samples": 3,
        "safety_checker": "no",
        "auto_hint": None,
        "seed": None,
        "webhook": None,
        "track_id": None,
        "scheduler": "DDPMScheduler",
        "base64": None,
        "clip_skip": 2,
        "controlnet_conditioning_scale": 0.35,
        "temp": None,
        "controlnet_type": "inpaint",
        "controlnet_model": "inpaint",
        "lora": None
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code == status.HTTP_200_OK:
            response_json = response.json()
            if "output" in response_json:
                return response_json["output"]
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Key 'output' not found in the response")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except httpx.RequestError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the request")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
@img_router.get('/{id}/{direction}', summary="Get one profile image")
async def get_profile_image(id: str, direction: str):
    img_path = f"./UPLOADS/{id}/{direction}.jpg"
    path_obj = Path(img_path)
    if not path_obj.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You need to upload the images")
    
    return FileResponse(img_path, media_type="image/jpeg")