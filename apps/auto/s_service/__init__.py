import numpy as np
import cv2
from ultralytics import YOLO

from apps.math import applyFormat
model = YOLO("./models/side_detect.pt")
def loadLandmark(id, Landmarks):
    path = f"./models/markset/{id}.pts"
    with open(path, 'r') as file:
        pts = file.read()

    samplePts = []
    for i, ptData in enumerate(pts[pts.index('{')+1:pts.index('}')].split('\n')):
        if ptData.strip() != '':
            x, y = map(float, ptData.strip().split())
            samplePts.append([x*512//800, y*512//800])

    for i, samplePt in enumerate(samplePts):
        Landmarks[i] = samplePt
    
    return Landmarks

def getProfileLandmarks(imgPath):
    profileLandmarks = np.zeros((30, 2, 2))

    image = cv2.imread(imgPath)
    results = model(image)
    keypoints_list = []

    for result in results:
        if result.keypoints is not None:
            keypoints = result.keypoints.xy.cpu().numpy()
            labels = result.keypoints.cls.cpu().numpy() if result.keypoints.cls is not None else np.zeros(len(keypoints))

            for kp, label in zip(keypoints, labels):
                for point, lbl in zip(kp, label):
                    x, y = point[:2]
                    keypoints_list.append({"x": float(x), "y": float(y), "label": int(lbl)})

            print(keypoints_list)    
    return applyFormat(profileLandmarks)

def mainProcess(id: str):
    return {"points":getProfileLandmarks(f"./UPLOADS/{id}/s.jpg")}
