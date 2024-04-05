import math
import numpy as np

def lineFromPoints(P, Q):
    A = Q['y'] - P['y']
    B = P['x'] - Q['x']
    C = A * P['x'] + B * P['y']
    return A, B, C

def getIntersection(A, B):
    A1, B1, C1 = lineFromPoints(A[0], A[1])
    A2, B2, C2 = lineFromPoints(B[0], B[1])
    determinant = A1 * B2 - A2 * B1
    if determinant == 0:
        return None
    else:
        x = (C1 * B2 - C2 * B1) / determinant
        y = (A1 * C2 - A2 * C1) / determinant
        return {'x': x, 'y': y}
    
def getSlope(point1, point2):
    try:
        return (point2['y'] - point1['y']) / (point2['x'] - point1['x'])
    except ZeroDivisionError:
        return float('inf')

def getParallel(a, ref):
    slope_ref = getSlope(ref[0], ref[1])
    if slope_ref == float('inf'):
        b = {'x': a['x'], 'y': a['y'] + 1}
    else:
        delta_x = 10
        delta_y = slope_ref * delta_x
        b = {'x': a['x'] + delta_x, 'y': a['y'] + delta_y}
    return b

def getVertical(a, ref):
    slope_ref = getSlope(ref[0], ref[1])
    if slope_ref == 0:
        b = {'x': a['x'], 'y': a['y'] + 1}
    elif slope_ref == float('inf'):
        b = {'x': a['x'] + 1, 'y': a['y']}
    else:
        slope_perpendicular = -1 / slope_ref
        delta_x = 10
        delta_y = slope_perpendicular * delta_x
        b = {'x': a['x'] + delta_x, 'y': a['y'] + delta_y}
    return b

def getAngle(a, b):
    slope1 = getSlope(a[0], a[1])
    slope2 = getSlope(b[0], b[1])
    angle = math.degrees(math.atan2(slope1 - slope2, 1 + slope1*slope2))
    if angle < 0:
        angle = angle + 180
    elif angle > 180:
        angle = angle - 180
    return angle

def getDistance(a, b):
    x = a['x'] - b['x']
    y = a['y'] - b['y']
    return math.sqrt(2 * (x**2 + y**2))

def getPosition(p, l):
    v = np.array([l[1]['x'] - l[0]['x'], l[1]['y'] - l[0]['y']])
    w = np.array([p['x'] - l[0]['x'], p['y'] - l[0]['y']])
    cross_product = np.cross(v, w)
    if cross_product > 0:
        return -1
    elif cross_product < 0:
        return 1
    else:
        return 0
    
def getDistanceP2L(p, l):
    v = np.array([l[1]['x'] - l[0]['x'], l[1]['y'] - l[0]['y']])
    w = np.array([p['x'] - l[0]['x'], p['y'] - l[0]['y']])
    cross_product = np.cross(v, w)
    distance = abs(cross_product) / np.linalg.norm(v)
    return distance
    
def getCenter(a, b):
    x = (a['x'] + b['x']) / 2
    y = (a['y'] + b['y']) / 2
    return {'x': x, 'y': y}

def getTL(a, b):
    x = min(a['x'], b['x'])
    y = min(a['y'], b['y'])
    return {'x': x, 'y': y}

def getBR(a, b):
    x = max(a['x'], b['x'])
    y = max(a['y'], b['y'])
    return {'x': x, 'y': y}

def getDistance(a, b):
    x = a['x'] - b['x']
    y = a['y'] - b['y']
    return math.sqrt(2 * (x**2 + y**2))

def getRectArea(c, r):  # center, radius
    TL = {'x': c['x'] - r, 'y': c['y'] - r}
    BR = {'x': c['x'] + r, 'y': c['y'] + r}
    return TL, BR

def applyFormat(points_array):
    temp_pts_array = []
    for points in points_array:
        temp_points = []
        for point in points:
            print(point)
            temp = {}
            temp['x'] = point[0]
            temp['y'] = point[1]
            temp_points.append(temp)
        temp_pts_array.append(temp_points)
    return temp_pts_array

async def CompleteMarkPoints(points, RLs):
    points[54][0] = getIntersection((points[49][0], points[52][0]), RLs[5])
    points[34][0] = getIntersection((points[40][0], points[35][0]), RLs[3])
    points[56][0] = getIntersection(RLs[4], RLs[6])
    return points