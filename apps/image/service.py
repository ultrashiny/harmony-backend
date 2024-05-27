import os
import timeit
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from PIL import Image
import io
from .measure.main import createReportImages

from apps.draw import GetCanva
import cv2
import mediapipe as mp
import numpy as np

def normalized_to_pixel_coordinates(normalized_x, normalized_y, image_width, image_height):
    """Converts normalized values to pixel coordinates."""
    x_px = min(max(int(normalized_x * image_width), 0), image_width - 1)
    y_px = min(max(int(normalized_y * image_height), 0), image_height - 1)
    return x_px, y_px

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
        
    @staticmethod
    async def generate_mask(id: str):
        mp_face_mesh = mp.solutions.face_mesh

        # Initialize MediaPipe Face Mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)
        
        # img_path = f"./UPLOADS/{id}/f.jpg"
        img_path = os.path.join("UPLOADS", str(id), "f.jpg")
        start_time = timeit.default_timer()
        image = cv2.imread(img_path)
        end_time = timeit.default_timer()
        print('----------------------Imread time', end_time - start_time)
        if image is None:
            raise FileNotFoundError(f"Image not found at {img_path}")
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = face_mesh.process(image_rgb)
        
        # Draw facial regions if landmarks were detected
        if results.multi_face_landmarks:
            for face_landmark in results.multi_face_landmarks:
                landmarks = []
                for landmark in face_landmark.landmark:
                    x, y = normalized_to_pixel_coordinates(landmark.x, landmark.y, image.shape[1], image.shape[0])
                    landmarks.append((x, y))
                    
                landmarks = np.array(landmarks, dtype=np.int32)
                hull = cv2.convexHull(landmarks)
                
                centroid = np.mean(hull, axis=0)
                
                expanded_hull = []
                for point in hull:
                    direction = point - centroid
                    norm = np.linalg.norm(direction)
                    if norm != 0:
                        normalized_direction = direction / norm
                        new_point = point + normalized_direction * 20
                        expanded_hull.append(new_point)
                    
                expanded_hull = np.array(expanded_hull, dtype=np.int32)
                
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                cv2.fillPoly(mask, [expanded_hull], 255)
                
                # masked_image = cv2.bitwise_and(image, image, mask=mask)
                
                # mask_url = f"./UPLOADS/{id}/mask.jpg"
                output_dir = os.path.join("UPLOADS", str(id))
                
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                mask_url = os.path.join(output_dir, "mask.jpg")
                cv2.imwrite(mask_url, mask)
        
    @staticmethod
    async def generate_canny(id: str):
        # img_path = f"./UPLOADS/{id}/f.jpg"
        img_path = os.path.join("UPLOADS", id, "f.jpg")
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not found at {img_path}")
        
        image = cv2.imread(img_path)
        if image is None:
            raise ValueError(f"Failed to load image from {img_path}")
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        edges = cv2.Canny(gray_image, 50, 150)
        
        output_dir = os.path.join("UPLOADS", id)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # canny_url = f"./UPLOADS/{id}/canny.jpg"
        canny_url = os.path.join(output_dir, "canny.jpg")
        cv2.imwrite(canny_url, edges)