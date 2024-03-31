import json
import os
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from PIL import Image
import io
from .measure.main import createReportImages

from apps.draw import GetCanva

class ImageService:
    @staticmethod
    async def save(dir, filename: str, src: UploadFile):
        try:
            img_path = dir / f"{filename}.jpg"
            buffer = await src.read()
            img = Image.open(io.BytesIO(buffer))
            img = img.convert('RGB')
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            img.save(img_path, "JPEG")
            await src.seek(0)
            return {"success": True}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save file as JPG: {e}")
        
    @staticmethod
    async def generate(id: str, points: list, lines: list):
        f = Path(f"./UPLOADS/{id}") / "f.jpg"
        s = Path(f"./UPLOADS/{id}") / "s.jpg"
        if not os.path.exists(f):
            f = Path(f"./UPLOADS/sample") / "f.jpg"
        if not os.path.exists(s):
            s = Path(f"./UPLOADS/sample") / "s.jpg"
        f_canva = GetCanva(f)
        s_canva = GetCanva(s)
        await createReportImages(id, f_canva, s_canva, points, lines)