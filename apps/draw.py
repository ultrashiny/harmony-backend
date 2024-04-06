import os
from PIL import Image, ImageDraw

from apps.math import getBR, getCenter, getDistance, getRectArea, getTL

ZERO = 0.0001

def GetCanva(url):
    if os.path.exists(url):
        img = Image.open(url)
        BACKGROUND_COLOR = (255, 255, 255)
        edge = max(img.height, img.width)
        offset = ((edge - img.width) // 2, (edge - img.height) // 2)
        canva = Image.new('RGB', (edge, edge), BACKGROUND_COLOR)
        canva.paste(img, offset)
        return canva
    return None

def GetAreaImage(canvas: Image, TL, BR, TARGET_SIZE = (300, 300)) -> Image:
    crop = canvas.crop((TL['x'], TL['y'], BR['x'], BR['y']))
    crop = crop.resize(TARGET_SIZE)
    return crop

def RemakePointArrayBaseOnCrop(TL, W, points, TARGET_WIDTH = 300):
    res_points = []
    for couple in points:
        res_couple = []
        for point in couple:
            x = (point['x'] - TL['x']) * TARGET_WIDTH / W
            y = (point['y'] - TL['y']) * TARGET_WIDTH / W
            res_couple.append({'x': x, 'y': y})
        res_points.append(res_couple)
    return res_points

def RemakePointArrayBaseOnImgSize(url, points):
    img = Image.open(url)
    SRC_LENGTH = 800
    TARGET_LENGTH = max(img.height, img.width)
    res_points = []
    for couple in points:
        res_couple = []
        for point in couple:
            src_x = point["x"]
            src_y = point["y"]
            target_x = src_x * TARGET_LENGTH / SRC_LENGTH
            target_y = src_y * TARGET_LENGTH / SRC_LENGTH
            res_couple.append({"x": target_x, "y": target_y})
        res_points.append(res_couple)
    return res_points

def GetFeatureArea(points, indexes, circular=False):
    TL = {"x": float('inf'), "y": float('inf')}   # Top, Left
    BR = {"x": float('-inf'), "y": float('-inf')}   # Bottom, Right

    for index in indexes:
        for point in points[index]:
            TL = getTL(TL, point)
            BR = getBR(BR, point)

    C = getCenter(TL, BR)   # Center
    R = getDistance(C, TL)  # Radius

    if circular:
        return C, R
    else:
        return getRectArea(C, R), R*2
    
def GetAreaImg(canvas: Image, TL, BR, TARGET_SIZE = (300, 300)) -> Image:
    crop = canvas.crop((TL['x'], TL['y'], BR['x'], BR['y']))
    crop = crop.resize(TARGET_SIZE)
    return crop

def UpdatePointArrayBaseOnCrop(TL, W, points_array, TARGET_WIDTH = 300):
    scale = TARGET_WIDTH / W
    for points in points_array:
        for couple in points:
            for point in couple:
                point['x'] = (point['x'] - TL['x']) * scale
                point['y'] = (point['y'] - TL['y']) * scale
    return points_array

def extendLine(x1, y1, x2, y2, length=1000):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        return (x1, y1 - length, x1, y2 + length)
    elif dy == 0:
        return (x1 - length, y1, x1 + length, y1)
    else:
        m = dy / dx
        b = y1 - m * x1
        x_start = x1 - length
        y_start = m * x_start + b
        x_end = x2 + length
        y_end = m * x_end + b
        return (x_start, y_start, x_end, y_end)
def DrawInfiniteLine(painter, a, b):
    stx, sty, edx, edy = extendLine(a['x'], a['y'], b['x'], b['y'])
    painter.line((stx, sty, edx, edy), fill=(57, 208, 192))
def DrawReferenceLines(painter:ImageDraw, RLs, indexes):
    for index in indexes:
        st = RLs[index][0]
        ed = RLs[index][1]
        DrawInfiniteLine(painter, st, ed)

def DrawDottedLine(painter, st, ed, space=10, color=(0, 255, 0), size=2):
    delta_x = ed['x'] - st['x']
    delta_y = ed['y'] - st['y']
    length = (delta_x**2 + delta_y**2)**0.5
    count_dots = int(length / space)
    step_x = delta_x / (count_dots + ZERO)
    step_y = delta_y / (count_dots + ZERO)
    for i in range(count_dots):
        x = st['x'] + i * step_x
        y = st['y'] + i * step_y
        painter.ellipse((x-size, y-size, x+size, y+size), fill=color)

def DrawSolidLine(painter, st, ed, color=(0, 255, 0), width=2):
    st = (st['x'], st['y'])
    ed = (ed['x'], ed['y'])
    painter.line([st, ed], fill=color, width=width)

def DrawDottedLines(painter:ImageDraw, lines, color=(0, 255, 0)):
    for line in lines:
        A = line[0]
        B = line[1]
        DrawDottedLine(painter, A, B, color=color)

def DrawSolidLines(painter:ImageDraw, lines):
    for line in lines:
        A = line[0]
        B = line[1]
        DrawSolidLine(painter, A, B)

def DrawPoint(painter, point, color=(255, 0, 0), size=2):
    painter.ellipse((point['x']-size, point['y']-size, point['x']+size, point['y']+size), color)

def DrawPoints(painter:ImageDraw, points):
    for point in points:
        DrawPoint(painter, point)