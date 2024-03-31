import numpy as np

from apps.math import applyFormat

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

def getProfileLandmarks(imgPath, id="sample"):
    profileLandmarks = np.zeros((30, 2, 2))
    profileLandmarks = loadLandmark(id, profileLandmarks)
    
    return applyFormat(profileLandmarks)

def mainProcess(id: str):
    return {"points":getProfileLandmarks(f"./UPLOADS/{id}/s.jpg")}
