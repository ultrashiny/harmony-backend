from apps.draw import DrawDottedLines, DrawPoints, DrawReferenceLines, DrawSolidLines, GetAreaImg, GetFeatureArea, UpdatePointArrayBaseOnCrop
from PIL import ImageDraw
from apps.math import getIntersection, getVertical

indexs_array = [
    # FRONT PROFILE FEATURES
    [[12, 17], []], # Eye Separation Ratio
    [[29, 19, 5, 1], [12, 13, 14, 15]], # Facial Thirds
    [[11, 16], [16]], # Lateral Canthal Tilt
    [[17, 21, 6], [17, 21]], # Facial WH Ratio
    [[26, 28], []], # Jaw Frontal Angle
    [[17], [9, 11, 17]], # Cheek Bone Height
    [[], []], # Total Facial WH Ratio - TODO
    [[], []], # Bigonial Width - TODO
    [[20, 29], [15, 17]], # ChinPhiltrunRatio
    [[], []], # Neck Width - TODO
    [[], []], # Mouth Nose Width Ratio - TODO
    [[12, 21], [17]], # Midface Ratio
    [[10, 14, 12, 8], [11]], # Eyebrow Position Ratio
    [[9, 16], [18, 19, 22, 23]], # Eye Spacing Ratio
    [[], []], # Eye Aspect Ratio - TODO
    [[25, 24, 21], [17]], # Lower Upper Lip Ratio
    [[], []], # Deviation Of IAA & JFA - TODO
    [[], []], # Eyebrow Tilt - TODO
    [[], []], # Bitemporal Width - TODO
    [[19, 24, 29], [14, 15, 20]], # Lower Third Proportion
    [[], []], # Ipsilaterl Alar Angle - TODO
    [[], []], # Medial Canthal Angle - TODO

    # SIDE PROFILE FEATURES
    [[38, 49, 52], []], # Gonial Angle
    [[32, 35, 39], []], # Nasofrontal Angle
    [[52, 49], [2]], # Mandibular Plane Angle
    [[38, 49, 54], [5]], # Ramus Mandible Ratio
    [[32, 43, 50], []], # Facial Convexity Glabella
    [[51, 53, 55], []], # Submental Cervical Angle
    [[50, 35, 39], []], # Naso Facial Angle
    [[45, 44, 41], []], # Naso Labial Angle
    [[33, 57, 46], []], # Orbital Vector
    [[32, 40, 50], []], # Total Facial Convexity
    [[58, 48, 50], []], # Mentolabial Angle
    [[35, 43, 50], []], # Facial Convexity Nasion
    [[34, 35, 40, 42], [3]], # Nasal Projection
    [[40, 56, 33, 42], [3, 4, 6]], # Nasal WH Ratio
    [[45, 47, 50, 40], []], # RickettsELine
    [[47, 50, 45], []], # HoldwayHLine
    [[59, 50, 45], []], # SteinerSLine
    [[43, 50, 45, 47], []], # BurstoneLine
    [[35, 50, 40], []], # Nasomental Angle
    [[46, 49], [2]], # Gonion Mouth Relationship
    [[35, 50], [5]], # Recession Relative Frankfort Plane
    [[31, 32], [7]], # Browridge Inclination Angle
    [[39, 40, 41], []], # Nasal Tip Angle
]


class FeatureImg:
    def __init__(self, index = 0, canva = None, points = None, lines = None, p_indexs = [], l_indexs = []) -> None:
        self.index = index
        self.canva = canva
        self.points = points
        self.lines = lines
        self.p_indexs = p_indexs
        self.l_indexs = l_indexs
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []

    def create(self):
        (TL, BR), W = GetFeatureArea(self.points, self.indexs)
        crop = GetAreaImg(self.canva, TL, BR)
        painter = ImageDraw.Draw(crop)
        [self.points, self.lines] = UpdatePointArrayBaseOnCrop(TL, W, [self.points, self.lines])
        self.set_draws()
        DrawReferenceLines(painter, self.lines, self.p_indexs)
        DrawDottedLines(painter, self.dot_lines)
        DrawSolidLines(painter, self.solid_lines)
        DrawPoints(painter, self.draw_points)

    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []

class FeatureImgEyeSeparationRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = [(self.points[12][0], self.points[12][1])]
        self.solid_lines  = [(self.points[17][0], self.points[17][1])]
        self.draw_points  = [self.points[12][0], self.points[12][1], 
                             self.points[17][0], self.points[17][1],]
        
class FeatureImgFacialThirds(FeatureImg):
    def set_draws(self):
        temp1 = getIntersection((self.points[1][0], getVertical(self.points[1][0], self.lines[13])), self.lines[13])
        temp2 = getIntersection((temp1, getVertical(temp1, self.lines[14])), self.lines[14])
        temp3 = getIntersection((temp2, getVertical(temp2, self.lines[15])), self.lines[15])
        
        self.dot_lines = [(self.points[1][0], temp1),
                          (temp1, temp2),
                          (temp2, temp3)]
        self.solid_lines = []
        self.draw_points = [self.points[29][0], self.points[19][0], 
                            self.points[5][0], self.points[1][0], 
                            temp1, temp2, temp3]

class FeatureImgLateralCanthalTilt(FeatureImg):
    def set_draws(self):
        self.dot_lines = [(self.points[11][0], self.points[16][0]),
                          (self.points[11][1], self.points[16][1]),]
        self.solid_lines = []
        self.draw_points = [self.points[11][0], self.points[11][1],
                            self.points[16][0], self.points[16][1],]
class FeatureImgFacialWHRatio(FeatureImg):
    def set_draws(self):
        temp = getIntersection((self.points[6][0], getVertical(self.points[6][0], self.lines[17])), self.lines[17])
        self.dot_lines = [(self.points[17][0], self.points[17][1]),]
        self.solid_lines = [(self.points[6][0], temp)]
        self.draw_points = [self.points[17][0], self.points[17][1],
                            self.points[6][0], self.points[21][0], temp]
class FeatureImgJawFrontalAngle(FeatureImg):
    def set_draws(self):
        temp = getIntersection((self.points[26][0], self.points[28][0]), (self.points[26][1], self.points[28][1]))
        self.dot_lines = [(self.points[26][0], temp),
                          (self.points[26][1], temp),]
        self.solid_lines = []
        self.draw_points = [self.points[26][0], self.points[26][1],
                            self.points[28][0], self.points[28][1], temp]
class FeatureImgCheekBoneHeight(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgTotalFacialWHRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgBigonialWidth(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgChinPhiltrumRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNeckWidth(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgMouthNoseWidthRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgMidfaceRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgEyebrowPositionRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgEyeSpacingRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgEyeAspectRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgLowerUpperLipRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgDeviationOfIaaJfa(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgEyebrowTilt(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgBitemporalWidth(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgLowerThirdProportion(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgIpsilateralAlarAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgMedialCanthalAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgGonialAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasofrontalAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgMandibularPlaneAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgRamusMandibleRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgFacialConvexityGlabella(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgSubmentalCervicalAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasoFacialAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasoLabialAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgOrbitalVector(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgTotalFacialConvexity(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgMentolabialAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgFacialConvexityNasion(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasalProjection(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasalWHRatio(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgRickettsELine(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgHoldawayHLine(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgSteinerSLine(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgBurstoneLine(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasomentalAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgGonionMouthRelationship(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgRecessionRelativeFrankfortPlane(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgBrowridgeInclinationAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []
class FeatureImgNasalTipAngle(FeatureImg):
    def set_draws(self):
        self.dot_lines = []
        self.solid_lines = []
        self.draw_points = []

class FeatureImgs:
    def __init__(self, f_canva = None, s_canva = None, points = None, lines = None) -> None:
        self.imgs = [
            FeatureImgEyeSeparationRatio(),
            FeatureImgFacialThirds(),
            FeatureImgLateralCanthalTilt(),
            FeatureImgFacialWHRatio(),
            FeatureImgJawFrontalAngle(),
            FeatureImgCheekBoneHeight(),
            FeatureImgTotalFacialWHRatio(),
            FeatureImgBigonialWidth(),
            FeatureImgChinPhiltrumRatio(),
            FeatureImgNeckWidth(),
            FeatureImgMouthNoseWidthRatio(),
            FeatureImgMidfaceRatio(),
            FeatureImgEyebrowPositionRatio(),
            FeatureImgEyeSpacingRatio(),
            FeatureImgEyeAspectRatio(),
            FeatureImgLowerUpperLipRatio(),
            FeatureImgDeviationOfIaaJfa(),
            FeatureImgEyebrowTilt(),
            FeatureImgBitemporalWidth(),
            FeatureImgLowerThirdProportion(),
            FeatureImgIpsilateralAlarAngle(),
            FeatureImgMedialCanthalAngle(),
            FeatureImgGonialAngle(),
            FeatureImgNasofrontalAngle(),
            FeatureImgMandibularPlaneAngle(),
            FeatureImgRamusMandibleRatio(),
            FeatureImgFacialConvexityGlabella(),
            FeatureImgSubmentalCervicalAngle(),
            FeatureImgNasoFacialAngle(),
            FeatureImgNasoLabialAngle(),
            FeatureImgOrbitalVector(),
            FeatureImgTotalFacialConvexity(),
            FeatureImgMentolabialAngle(),
            FeatureImgFacialConvexityNasion(),
            FeatureImgNasalProjection(),
            FeatureImgNasalWHRatio(),
            FeatureImgRickettsELine(),
            FeatureImgHoldawayHLine(),
            FeatureImgSteinerSLine(),
            FeatureImgBurstoneLine(),
            FeatureImgNasomentalAngle(),
            FeatureImgGonionMouthRelationship(),
            FeatureImgRecessionRelativeFrankfortPlane(),
            FeatureImgBrowridgeInclinationAngle(),
            FeatureImgNasalTipAngle(),
        ]
        for i, indexs in enumerate(indexs_array):
            self.imgs[i] = FeatureImg(i, f_canva if i < 22 else s_canva, points, lines, indexs[0], indexs[1])
        