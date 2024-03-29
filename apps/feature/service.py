from apps.feature.measure import Measures
from apps.math import getIntersection, getParallel, getVertical
from .schemas import FeaturePoints

class FeatureService:
    @staticmethod
    async def calculate(data: FeaturePoints) -> dict:
        reference_lines = await FeatureService.get_reference_lines(data.points)
        points = await FeatureService.process_points(data.points, reference_lines)
        measures = Measures(data.race, data.gender, points, reference_lines)
        return {
            "values": measures.get_values(),
            "lines": reference_lines,
        }
    
    async def get_reference_lines(points):
        # Define reference line and set the None for the first
        reference_lines = [({'x': 0, 'y': 0}, {'x': 0, 'y': 0})]

        # 1th Reference Line
        ref = (points[37][0], points[38][0])
        reference_lines.append(ref)

        # 2nd - 8th Reference Lines
        indexs  = [49, 42, 40, 50, 33, 32, 33]
        flags   = [ 0,  1,  1,  1,  0,  1,  1]
        for index, flag in zip(indexs, flags):
            a = points[index][0]
            b = getVertical(a, ref) if flag else getParallel(a, ref)
            reference_lines.append((a,b))

        # 9th - 23th Reference Lines
        ref = (points[1][0], points[29][0])
        indexs  = [17,  7, 12, 1, 5, 19, 29, 16, 21, 9, 9, 24, 6, 16, 16]
        flags   = [-1, -1, -1, 0, 0,  0,  0, -1,  0, 1, 2,  0, 0,  1,  2]
        for index, flag in zip(indexs, flags):
            a = points[index][0]
            if flag == -1:
                b = points[index][1]
            elif flag == 0:
                b = getVertical(a, ref)
            elif flag == 1:
                b = getParallel(a, ref)
            elif flag == 2:
                a = points[index][1]
                b = getParallel(a, ref)
            reference_lines.append((a, b))
        
        # 24th Reference Line
        reference_lines.append(ref)
        return reference_lines
    
    async def process_points(points, RLs):
        points[54][0] = getIntersection((points[49][0], points[52][0]), RLs[5])
        points[34][0] = getIntersection((points[40][0], points[35][0]), RLs[3])
        points[56][0] = getIntersection(RLs[4], RLs[6])
        return points
    
    
