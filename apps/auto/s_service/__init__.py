import numpy as np

def loadLandmark(id, Landmarks):
    path = f"./models/markset/{id}.pts"
    with open(path, 'r') as file:
        pts = file.read()

    samplePts = []
    for i, ptData in enumerate(pts[pts.index('{')+1:pts.index('}')].split('\n')):
        if ptData.strip() != '':
            x, y = map(float, ptData.strip().split())
            samplePts.append([x, y])

    for i, samplePt in enumerate(samplePts):
        Landmarks[i] = samplePt
    
    return Landmarks

def getProfileLandmarks(imgPath, id="sample"):
    profileLandmarks = np.zeros((30, 2))
    profileLandmarks = loadLandmark(id, profileLandmarks)
    
    return profileLandmarks.tolist()

def mainProcess(id: str):
    return {"points":getProfileLandmarks(f"./UPLOADS/{id}/s.jpg")}
