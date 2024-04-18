from apps.math import getAngle, getCenter, getDistance, getDistanceP2L, getIntersection, getPosition, getVertical

features = [
    "EyeSeparationRatio",
    "FacialThirds",
    "LateralCanthalTilt",
    "FacialWHRatio",
    "JawFrontalAngle",
    "CheekBoneHeight",
    "TotalFacialWHRatio",
    "BigonialWidth",
    "ChinPhiltrumRatio",
    "NeckWidth",
    "MouthNoseWidthRatio",
    "MidfaceRatio",
    "EyebrowPositionRatio",
    "EyeSpacingRatio",
    "EyeAspectRatio",
    "LowerUpperLipRatio",
    "DeviationOfIaaJfa",
    "EyebrowTilt",
    "BitemporalWidth",
    "LowerThirdProportion",
    "IpsilateralAlarAngle",
    "MedialCanthalAngle",
    
    "GonialAngle",
    "NasofrontalAngle",
    "MandibularPlaneAngle",
    "RamusMandibleRatio",
    "FacialConvexityGlabella",
    "SubmentalCervicalAngle",
    "NasoFacialAngle",
    "NasoLabialAngle",
    "OrbitalVector",
    "TotalFacialConvexity",
    "MentolabialAngle",
    "FacialConvexityNasion", 
    "NasalProjection", 
    "NasalWHRatio", 
    "RickettsELine",
    "HoldawayHLine",
    "SteinerSLine",
    "BurstoneLine",
    "NasomentalAngle",
    "GonionMouthRelationship",
    "RecessionRelativeFrankfortPlane",
    "BrowridgeInclinationAngle",
    "NasalTipAngle",
]

class Measure:
    def __init__(self, race = 0, gender = 0, name = None, points = None, lines = None):
        self.race = race
        self.gender = gender
        self.name = name
        self.points = points
        self.lines = lines
        self.value = None
        self.minArray = None
        self.maxArray = None
        self.array = None
        self.ideal = None

    def get(self):
        if isinstance(self.value, float):
            self.value = round(self.value, 2)
        elif isinstance(self.value, list):
            update = []
            for t in self.value:
                if isinstance(t, float):
                    t = round(t, 2)
                    update.append(t)
            self.value = update
        return {
            "measure": self.name,
            "value": self.value,
            "index": self.get_index(),
            "ideal": self.ideal
        }
    
    def get_index(self):
        if self.array is None:
            result = self.minArray[self.gender][0] + self.thresholds[self.race]
            self.ideal = f"{result:.2f} - "
            result = self.maxArray[self.gender][0] + self.thresholds[self.race]
            self.ideal += f"{result:.2f}"
            for i in range(len(self.minArray[0])):
                min = self.minArray[self.gender][i] + self.thresholds[self.race]
                max = self.maxArray[self.gender][i] + self.thresholds[self.race]
                if self.value >= min and self.value <= max:
                    return i
            return i
        else:
            self.ideal = self.array[0]
            for i in range(len(self.array)):
                if self.value == self.array[i]:
                    return i
            return i
    
class MeasureGonialAngle(Measure):
    def calc(self):
        a = (self.points[38][0], self.points[49][0])
        b = (self.points[52][0], self.points[49][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, 0, 4, 0, 0, 0, 0]
        self.minArray = [[112, 109.5, 106, 102, 97, 92, 80],[114, 111, 108, 104, 99, 94, 80]]
        self.maxArray = [[123, 125.5, 129, 133, 138, 143, 160],[125, 128, 131, 135, 140, 146, 160]]

class MeasureNasofrontalAngle(Measure):
    def calc(self):
        a = (self.points[32][0], self.points[35][0])
        b = (self.points[39][0], self.points[35][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, -4, 4, 0, 0, 4, 0]
        self.minArray = [[106, 101, 97, 94, 88, 70], [122, 117, 113, 110, 107, 70]]
        self.maxArray = [[129, 134, 138, 141, 147, 170], [143, 148, 152, 155, 158, 170]]

class MeasureMandibularPlaneAngle(Measure):
    def calc(self):
        a = (self.lines[2][0], self.lines[2][1])
        b = (self.points[52][0], self.points[49][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, 0, 2, 0, 0, 0, 0]
        self.minArray = [[15, 14, 12.5, 10, 8, 0], [15, 14, 12.5, 10, 8, 0]]
        self.maxArray = [[22, 27, 30, 32.5, 35, 45], [23, 27, 30, 32.5, 35, 45]]

class MeasureRamusMandibleRatio(Measure):
    def calc(self):
        a = getDistance(self.points[38][0], self.points[49][0])
        b = getDistance(self.points[54][0], self.points[49][0])
        self.value = a / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[0.59, 0.54, 0.49, 0.41, 0.33, 0.1],[0.52, 0.48, 0.42, 0.34, 0.26, 0.1]]
        self.maxArray = [[0.78, 0.83, 0.88, 0.96, 1.04, 1.5],[0.70, 0.75, 0.8, 0.88, 0.96, 1.5]]

class MeasureFacialConvexityGlabella(Measure):
    def calc(self):
        a = (self.points[32][0], self.points[43][0])
        b = (self.points[50][0], self.points[43][0])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, 2, 1, -2, 3, -3, 0]
        self.minArray = [[168, 161, 163, 160, 155, 140], [166, 163, 161, 159, 155, 140]]
        self.maxArray = [[176, 179, 181, 183, 184, 195], [175, 178, 180, 182, 184, 195]]

class MeasureSubmentalCervicalAngle(Measure):
    def calc(self):
        a = (self.points[51][0], self.points[53][0])
        b = (self.points[55][0], self.points[53][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[91, 81, 81, 75, 50], [91, 81, 81, 75, 50]]
        self.maxArray = [[110, 120, 130, 140, 160], [110, 120, 130, 140, 160]]

class MeasureNasoFacialAngle(Measure):
    def calc(self):
        a = (self.points[39][0], self.points[35][0])
        b = (self.points[50][0], self.points[35][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, 2, -3, 0, 0, 0, 0]
        self.minArray = [[30, 36, 28, 26.5, 25.5, 10], [30, 36, 28, 26.5, 25.5, 10]]
        self.maxArray = [[36, 40, 42, 43.5, 44.5, 60], [36, 40, 42, 43.5, 44.5, 60]]

class MeasureNasoLabialAngle(Measure):
    def calc(self):
        a = (self.points[41][0], self.points[44][0])
        b = (self.points[45][0], self.points[44][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, -11, -4, 6, 4, -8, 0]
        self.minArray = [[94, 90, 85, 81, 70, 65, 30], [96, 92, 87, 83, 79, 74, 30]]
        self.maxArray = [[117, 121, 126, 130, 140, 150, 190],[118, 122, 127, 131, 144, 154, 190]]

class MeasureOrbitalVector(Measure):
    def calc(self):
        p = self.points[57][0]
        l = self.lines[8]
        position = getPosition(p, l)
        distance = getDistanceP2L(p, l)
        if distance <= 2:
            self.value = "neutral"
        else:
            if position == -1:
                self.value = "positive"
            if position == 1:
                self.value = "negative"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["positive", "neutral", "negative"]     

class MeasureTotalFacialConvexity(Measure):
    def calc(self):
        a = (self.points[32][0], self.points[40][0])
        b = (self.points[50][0], self.points[40][0])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, 5, 4, -1, 2, -3, 0]
        self.minArray = [[137.5, 135.5, 132.5, 129.5, 126.5, 124.5, 100],[137.5, 135.5, 132.5, 129.5, 126.5, 124.5, 100]]
        self.maxArray = [[148.5, 150.5, 153.5, 156.5, 159.5, 161.5, 180],[148.5, 150.5, 153.5, 156.5, 159.5, 161.5, 180]]

class MeasureMentolabialAngle(Measure):
    def calc(self):
        a = (self.points[58][0], self.points[48][0])
        b = (self.points[50][0], self.points[48][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[108, 94, 80, 75, 65, 40], [93, 79, 70, 65, 62, 40]]
        self.maxArray = [[130, 144, 158, 165, 175, 200], [125, 139, 153, 160, 175, 200]]

class MeasureFacialConvexityNasion(Measure):
    def calc(self):
        a = (self.points[35][0], self.points[43][0])
        b = (self.points[50][0], self.points[43][0])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, 2, 1, -2, 3, -3, 0]
        self.minArray = [[163, 160, 158, 155, 152, 120], [161, 158, 156, 153, 152, 120]]
        self.maxArray = [[170, 173, 175, 178, 181, 195], [170, 173, 175, 178, 181, 195]]

class MeasureNasalProjection(Measure):
    def calc(self):
        temp = getIntersection((self.points[40][0], getVertical(self.points[40][0], self.lines[3])), self.lines[3])
        a = getDistance(self.points[40][0], temp)
        b = getDistance(self.points[40][0], self.points[34][0])
        self.value = a / b
        self.thresholds = [0, -0.1, -0.1, 0, -0.07, 0, 0]
        self.minArray = [[0.55, 0.5, 0.45, 0.37, 0.3, 0.1],[0.52, 0.47, 0.42, 0.34, 0.3, 0.1]]
        self.maxArray = [[0.68, 0.75, 0.78, 0.86, 0.95, 1.4],[0.68, 0.75, 0.78, 0.86, 0.95, 1.4]]

class MeasureNasalWHRatio(Measure):
    def calc(self):
        temp = getIntersection((self.points[40][0], getVertical(self.points[40][0], self.lines[3])), self.lines[3])
        a = getDistance(self.points[40][0], temp)
        b = getDistance(self.points[40][0], self.points[56][0])
        self.value = a / b
        self.thresholds = [0, -0.05, -0.12, 0, -0.03, -0.03, 0]
        self.minArray = [[0.62, 0.55, 0.49, 0.45, 0.4, 0.1],[0.68, 0.61, 0.55, 0.51, 0.45, 0.1]]
        self.maxArray = [[0.88, 0.95, 1.01, 1.05, 1.1, 1.6],[0.93, 1.0, 1.06, 1.1, 1.13, 1.6]]

class MeasureRickettsELine(Measure):
    def calc(self):
        a = getPosition(self.points[45][0], (self.points[40][0], self.points[50][0]))
        b = getPosition(self.points[47][0], (self.points[40][0], self.points[50][0]))
        if a * b != 1:
            self.value = "unideal"
        else:
            a = getDistanceP2L(self.points[45][0], (self.points[40][0], self.points[50][0]))
            b = getDistanceP2L(self.points[47][0], (self.points[40][0], self.points[50][0]))
            r = a / b
            if r >= 1.5 and r <= 2.5:
                self.value = "ideal"
            elif r >= 1 and r <= 1.5:
                self.value = "near ideal"
            elif r >= 2.5 and r <= 3:
                self.value = "near ideal"
            else:
                self.value = "unideal"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["ideal", "near ideal", "unideal"]

class MeasureHoldawayHLine(Measure):
    def calc(self):
        a = getDistanceP2L(self.points[47][0], (self.points[45][0], self.points[50][0]))
        if a <= 6:
            self.value = "ideal"
        elif a <= 15:
            self.value = "near ideal"
        else:
            self.value = "unideal"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["ideal", "near ideal", "unideal"]

class MeasureSteinerSLine(Measure):
    def calc(self):
        a = getDistanceP2L(self.points[45][0], (self.points[59][0], self.points[50][0]))
        if a <= 6:
            self.value = "ideal"
        elif a <= 15:
            self.value = "near ideal"
        else:
            self.value = "unideal"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["ideal", "near ideal", "unideal"]

class MeasureBurstoneLine(Measure):
    def calc(self):
        a = getDistanceP2L(self.points[45][0], (self.points[43][0], self.points[50][0]))
        b = getDistanceP2L(self.points[47][0], (self.points[43][0], self.points[50][0]))
        c = a / b
        if c >= 1.3 and c <= 1.8:
            self.value = "ideal"
        elif c >= 1.1 and c <= 1.3:
            self.value = "near ideal"
        elif c >= 1.8 and c <= 2:
            self.value = "near ideal"
        else:
            self.value = "unideal"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["ideal", "near ideal", "unideal"]

class MeasureNasomentalAngle(Measure):
    def calc(self):
        a = (self.points[35][0], self.points[40][0])
        b = (self.points[50][0], self.points[40][0])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, -3, 3, 0, 0, 0, 0]
        self.minArray = [[125, 120, 118, 116, 114, 100], [125, 120, 118, 116, 114, 100]]
        self.maxArray = [[132, 133.5, 134.5, 136.5, 138.5, 150],[132, 133.5, 134.5, 136.5, 138.5, 150]]

class MeasureGonionMouthRelationship(Measure):
    def calc(self):
        self.value = "below"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["below", "in line", "above", "notably above"]

class MeasureRecessionRelativeFrankfortPlane(Measure):
    def calc(self):
        if getPosition(self.points[35][0], self.lines[5]):
            self.value = "none"
        else:
            d = getDistanceP2L(self.points[35][0], self.lines[5])
            if d <= 4:
                self.value = "slight"
            elif d <= 8:
                self.value = "moderate"
            else:
                self.value = "extreme"
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.array = ["none", "slight", "moderate", "extreme"]

class MeasureBrowridgeInclinationAngle(Measure):
    def calc(self):
        a = (self.lines[7][0], self.lines[7][1])
        b = (self.points[32][0], self.points[31][0])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[13, 10, 8, 6, 4, 2, 0], [10, 7, 5, 3, 1, 1, 0]]
        self.maxArray = [[24, 27, 29, 31, 33, 36, 45], [22, 25, 27, 29, 31, 39, 45]]

class MeasureNasalTipAngle(Measure):
    def calc(self):
        a = (self.points[36][0], self.points[40][0])
        b = (self.points[41][0], self.points[40][0])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, 0, 0, 0, 0, -10, 0]
        self.minArray = [[112, 108, 104, 100, 97, 70], [118, 115, 111, 108, 105, 70]]
        self.maxArray = [[125, 129, 133, 137, 140, 170], [131, 134, 138, 141, 144, 170]]

class MeasureEyeSeparationRatio(Measure):
    def calc(self):
        a = getDistance(self.points[12][0], self.points[12][1])
        b = getDistance(self.points[17][0], self.points[17][1])
        self.value = a * 100 / b
        self.thresholds = [0, 1, -0.7, 0, 0, 0, 0]
        self.minArray = [[44.3, 43.6, 43.1, 42.6, 42, 41, 35],[45, 44.3, 43.8, 43.3, 42.7, 42, 35]]
        self.maxArray = [[47.7, 48.4, 48.9, 49.4, 50, 51, 58],[47.9, 48.6, 49.1, 49.6, 50.2, 51, 58]]

class MeasureFacialThirds(Measure):
    def calc(self):
        a = getDistance(self.points[5][0], self.points[1][0])
        b = getDistance(self.points[19][0], self.points[5][0])
        c = getDistance(self.points[29][0], self.points[19][0])
        s = a + b + c
        self.value = [x * 100 for x in [a/s, b/s, c/s]]
        self.thresholds = [0, 1, -0.7, 0, 0, 0, 0]
        self.minArray = [[[31.5, 30.5, 29, 26.5, 25, 24, 18],[31.5, 31, 29.5, 29.5, 28, 27, 18]],
                         [[29.5, 28, 26.5, 25, 23.5, 22.5, 18],[30, 29.5, 27, 25, 24, 23, 18]]]
        self.maxArray = [[[34.5, 35.5, 37, 39.5, 41, 42, 50],[34.5, 35, 36.5, 37.5, 38, 39, 50]],
                         [[36.5, 38, 39.5, 41, 42.5, 43.5, 50],[36, 37.5, 39, 41, 42, 43, 50]]]
    
    def get_index(self):
        if self.gender == 0: # Male
            self.ideal = f"{self.minArray[self.value[2] == max(self.value)][self.gender][0] + self.thresholds[self.race]} - "
            self.ideal += f"{self.maxArray[self.value[2] == max(self.value)][self.gender][0] + self.thresholds[self.race]}"
            for i in range(len(self.minArray)):
                if all(x > self.minArray[self.value[2] == max(self.value)][self.gender][i] + self.thresholds[self.race] and x < self.maxArray[self.value[2] == max(self.value)][self.gender][i] + self.thresholds[self.race] for x in self.value):
                    return i
            return i
        else:
            self.ideal = f"{self.minArray[self.value[2] != max(self.value)][self.gender][0] + self.thresholds[self.race]} - "
            self.ideal += f"{self.maxArray[self.value[2] != max(self.value)][self.gender][0] + self.thresholds[self.race]}"
            for i in range(len(self.minArray)):
                if all(x > self.minArray[self.value[2] != max(self.value)][self.gender][i] + self.thresholds[self.race] and x < self.maxArray[self.value[2] != max(self.value)][self.gender][i] + self.thresholds[self.race] for x in self.value):
                    return i
            return i

class MeasureLateralCanthalTilt(Measure):
    def calc(self):
        a0 = (self.lines[16][1], self.lines[16][0])
        b0 = (self.points[16][0], self.points[11][0])
        a1 = (self.lines[16][0], self.lines[16][1])
        b1 = (self.points[11][1], self.points[16][1])
        l = 180 - getAngle(a0, b0)
        r = getAngle(a1, b1)
        self.value = (l + r) / 2
        self.thresholds = [0, 1.5, 2, 0, 0, 0, 0]
        self.minArray = [[5.2, 4, 3, 0, -2, -4, -10], [6, 4.8, 3.6, 1.5, 0, -3, -10]]
        self.maxArray = [[8.5, 9.7, 10.7, 13.7, 15.7, 17.9, 25],[9.6, 10.8, 12, 14.1, 15.6, 18.2, 25]]

class MeasureFacialWHRatio(Measure):
    def calc(self):
        a = getDistance(self.points[17][0], self.points[17][1])
        b = getDistance(self.points[21][0], self.points[6][0])
        self.value = a / b
        self.thresholds = [0, 0.03, -0.04, 0.02, 0, 0, 0]
        self.minArray = [[1.9, 1.85, 1.8, 1.75, 1.7, 1.66, 1.3],[1.9, 1.85, 1.8, 1.75, 1.7, 1.66, 1.3]]
        self.maxArray = [[2.06, 2.11, 2.16, 2.21, 2.26, 2.3, 2.8],[2.06, 2.11, 2.16, 2.21, 2.26, 2.3, 2.8]]

class MeasureJawFrontalAngle(Measure):
    def calc(self):
        a = (self.points[26][0], self.points[28][0])
        b = (self.points[26][1], self.points[28][1])
        self.value = 180 - getAngle(a, b)
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[84.5, 80.5, 76.5, 72.5, 69.5, 66.5, 40],[86, 82.5, 79, 75.5, 72, 69, 40]]
        self.maxArray = [[95, 99, 103, 107, 110, 113, 150],[97, 100.5, 104, 107.5, 111, 114, 150]]

class MeasureCheekBoneHeight(Measure):
    def calc(self):
        a = getDistance(self.points[21][0], getCenter(self.points[17][0], self.points[17][1]))
        b = getDistance(self.points[21][0], getCenter(self.points[12][0], self.points[12][1]))
        self.value = a * 100 / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[81, 76, 70, 65, 60, 55, 10], [83, 79, 73, 68, 63, 58, 10]]
        self.maxArray = [[100, 81, 76, 70, 65, 60, 55], [100, 83, 79, 73, 68, 63, 58]]

class MeasureTotalFacialWHRatio(Measure):
    def calc(self):
        a = getDistance(self.points[1][0], self.points[29][0])
        b = getDistance(self.points[17][0], self.points[17][1])
        self.value = a / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[1.33, 1.3, 1.26, 1.23, 1.2, 1.18, 1.0],[1.29, 1.26, 1.22, 1.19, 1.17, 1.15, 1.0]]
        self.maxArray = [[1.38, 1.41, 1.45, 1.48, 1.51, 1.53, 1.7],[1.35, 1.38, 1.42, 1.45, 1.47, 1.49, 1.7]]

class MeasureBigonialWidth(Measure):
    def calc(self):
        a = getDistance(self.points[22][0], self.points[22][1])
        b = getDistance(self.points[17][0], self.points[17][1])
        self.value = a * 100 / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[85.5, 83.5, 80.5, 77.5, 75, 70, 50],[81.5, 79.5, 76.5, 73.5, 70.5, 69, 50]]
        self.maxArray = [[92, 94, 97, 100, 102.5, 105, 120],[88.5, 90.5, 93.5, 96.5, 99.5, 102, 120]]

class MeasureChinPhiltrumRatio(Measure):
    def calc(self):
        a = getDistanceP2L(self.points[25][0], self.lines[15])
        b = getDistanceP2L(self.points[20][0], self.lines[17])
        self.value = a / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[2.05, 1.87, 1.75, 1.55, 1.2, 1.0, 0.1],[2.0, 1.85, 1.7, 1.5, 1.2, 1.0, 0, 1]]
        self.maxArray = [[2.55, 2.73, 2.85, 3.2, 3.55, 3.85, 5.0],[2.5, 2.65, 2.8, 3.15, 3.5, 3.8, 5.0]]
        
class MeasureNeckWidth(Measure):
    def calc(self):
        a = getDistance(self.points[27][0], self.points[27][1])
        b = getDistance(self.points[22][0], self.points[22][1])
        self.value = a * 100 / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[90, 85, 80, 75, 70, 65, 30], [75, 69, 67, 65, 62, 57, 30]]
        self.maxArray = [[100, 102, 105, 107, 75, 70, 130],[87, 93, 95, 97, 100, 103, 130]]

class MeasureMouthNoseWidthRatio(Measure):
    def calc(self):
        a = getDistance(self.points[23][0], self.points[23][1])
        b = getDistance(self.points[18][0], self.points[18][1])
        self.value = a / b
        self.thresholds = [0, -0.05, -0.04, 0, -0.03, 0, 0]
        self.minArray = [[1.38, 1.34, 1.3, 1.26, 1.22, 1.18, 0.9],[1.45, 1.4, 1.35, 1.3, 1.25, 1.21, 0.9]]
        self.maxArray = [[1.53, 1.57, 1.61, 1.65, 1.69, 1.73, 2.2],[1.67, 1.72, 1.77, 1.82, 1.87, 1.91, 2.2]]

class MeasureMidfaceRatio(Measure):
    def calc(self):
        a = getDistance(self.points[12][0], self.points[12][1])
        b = getDistance(self.points[21][0], getCenter(self.points[12][0], self.points[12][1]))
        self.value = a / b
        self.thresholds = [0, 0.02, 0.02, 0, 0, 0, 0]
        self.minArray = [[0.93, 0.9, 0.88, 0.85, 0.8, 0.77, 0.5],[1.0, 0.97, 0.95, 0.92, 0.87, 0.84, 0.5]]
        self.maxArray = [[1.01, 1.04, 1.06, 1.09, 1.14, 1.17, 1.5],[1.1, 1.13, 1.15, 1.18, 1.23, 1.26, 1.5]]

class MeasureEyebrowPositionRatio(Measure):
    def calc(self):
        a1 = getDistanceP2L(self.points[8][0], (self.points[12][0], self.points[12][1]))
        a2 = getDistanceP2L(self.points[8][1], (self.points[12][0], self.points[12][1]))
        b1 = getDistance(self.points[10][0], self.points[14][0])
        b2 = getDistance(self.points[10][1], self.points[14][1])
        self.value = (a1 / b1 + a2 / b2) / 2
        self.thresholds = [0, 0, 0.3, 0, 0, 0, 0]
        self.minArray = [[0, 0.65, 0.95, 1.2, 1.5, 1.8, 2.1],[0.4, 0.3, 0, 1.15, 1.35, 1.85, 2.1]]
        self.maxArray = [[0.65, 0.95, 1.2, 1.5, 1.8, 2.1, 4.0],[0.85, 1, 1.35, 1.75, 2, 2.3, 4.0]]
        
class MeasureEyeSpacingRatio(Measure):
    def calc(self):
        a = self.points[16][1]['x'] - self.points[16][0]['x']
        b1 = self.points[16][0]['x'] - self.points[9][0]['x']
        b2 = self.points[9][1]['x'] - self.points[16][1]['x']
        self.value = (a / b1 + a / b2) / 2
        self.thresholds = [0.02, 0.02, 0.32, 0.02, 0.02, 0.02, 0.02]
        self.minArray = [[0.93, 0.88, 0.83, 0.78, 0.67, 0.62, 0.42],[0.93, 0.88, 0.83, 0.78, 0.67, 0.62, 0.42]]
        self.maxArray = [[1.04, 1.07, 1.10, 1.17, 1.23, 1.43, 2.03],[1.04, 1.07, 1.10, 1.17, 1.23, 1.43, 2.03]]

class MeasureEyeAspectRatio(Measure):
    def calc(self):
        a1 = getDistance(self.points[16][1], self.points[11][1])
        b1 = getDistance(self.points[10][1], self.points[14][1])
        a2 = getDistance(self.points[16][0], self.points[11][0])
        b2 = getDistance(self.points[10][0], self.points[14][0])
        self.value = (a1 / b1 + a2 / b2) / 2
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[2.8, 2.6, 2.4, 2.2, 2, 1.8, 0],[2.55, 2.35, 2.15, 1.95, 1.75, 1.8, 0]]
        self.maxArray = [[3.6, 3.8, 4, 4.2, 4.4, 4.6, 6],[3.2, 3.4, 3.6, 3.8, 4.0, 4.6, 6]]

class MeasureLowerUpperLipRatio(Measure):
    def calc(self):
        a = self.points[25][0]['y'] - self.points[24][0]['y']
        b = self.points[24][0]['y'] - self.points[21][0]['y']
        self.value = a / b
        self.thresholds = [0, -0.2, 0, 0, 0, 0, 0]
        self.minArray = [[1.4, 1.1, 0.9, 0.7, 0.4, 0.1, 0.1],[1.35, 1.05, 0.85, 0.75, 0.35, 0.1, 0.1]]
        self.maxArray = [[2.0, 2.3, 2.5, 2.7, 3.0, 3.5, 5],[2.0, 2.3, 2.5, 2.7, 3.0, 3.5, 5]]

class MeasureDeviationOfIaaJfa(Measure):
    def calc(self):
        a0 = (self.points[26][0], self.points[28][0])
        a1 = (self.points[26][1], self.points[28][1])
        b0 = (self.points[9][0], self.points[19][0])
        b1 = (self.points[9][1], self.points[19][0])
        self.value = abs(getAngle(a0, a1) - getAngle(b0, b1))
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[0, 2.5, 5, 10, 15, 20], [0, 2.5, 5, 10, 15, 20]]
        self.maxArray = [[2.5, 5, 10, 15, 20, 100], [2.5, 5, 10, 15, 20, 100]]

class MeasureEyebrowTilt(Measure):
    def calc(self):
        a = getAngle((self.points[7][0], self.points[4][0]), self.lines[10])
        b = 180 - getAngle((self.points[7][1], self.points[4][1]), self.lines[10])
        self.value = (a + b) / 2
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[5, 3, 0, -2, -4, -15], [11, 9, 6, 4, 2, -15]]
        self.maxArray = [[13, 15, 18, 20, 22, 40], [18.7, 20.7, 23.7, 25.7, 27.7, 40]]

class MeasureBitemporalWidth(Measure):
    def calc(self):
        a = getDistance(self.points[2][0], self.points[2][1])
        b = getDistance(self.points[17][0], self.points[17][1])
        self.value = a * 100 / b
        self.thresholds = [0, 0, 0, -2, 0, 0, 0]
        self.minArray = [[84, 82, 79, 77, 74, 71, 50], [79, 76, 73, 70, 67, 65, 50]]
        self.maxArray = [[95, 97, 100, 102, 105, 108, 125],[92, 95, 98, 101, 104, 106, 125]]

class MeasureLowerThirdProportion(Measure):
    def calc(self):
        a = self.points[24][0]['y'] - self.points[19][0]['y']
        b = self.points[29][0]['y'] - self.points[19][0]['y']
        self.value = a * 100 / b
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[30.6, 29.6, 28.4, 27.2, 26.6, 20],[31.2, 30.2, 29.2, 28.2, 27.2, 20]]
        self.maxArray = [[34, 35, 36.2, 37.4, 38, 45], [34.5, 35.5, 36.5, 37.5, 38.5, 45]]

class MeasureIpsilateralAlarAngle(Measure):
    def calc(self):
        a = (self.points[9][1], self.points[19][0])
        b = (self.points[9][0], self.points[19][0])
        self.value = getAngle(a, b)
        self.thresholds = [0, 0, 0, 0, 0, 0, 0]
        self.minArray = [[84, 82, 79, 77, 75, 73, 50], [84, 82, 79, 77, 75, 73, 50]]
        self.maxArray = [[95, 97, 100, 102, 104, 106, 150],[95.5, 97.5, 100.5, 102.5, 104.5, 106.5, 150]]

class MeasureMedialCanthalAngle(Measure):
    def calc(self):
        a0 = (self.points[13][0], self.points[16][0])
        a1 = (self.points[15][0], self.points[16][0])
        b0 = (self.points[13][1], self.points[16][1])
        b1 = (self.points[15][1], self.points[16][1])
        self.value = (getAngle(a0, a1) + (180 - getAngle(b0, b1))) / 2
        self.thresholds = [0, 0, 8, 0, 0, 0, 0]
        self.minArray = [[20, 17, 15, 13, 11, 9, 5], [22, 20, 17, 15, 13, 11, 5]]
        self.maxArray = [[42, 50, 56, 63, 69, 75, 120], [44, 52, 58, 65, 71, 77, 120]]

class Measures:
    def __init__(self, race, gender, points, lines):
        self.measures = [
            MeasureEyeSeparationRatio(),
            MeasureFacialThirds(),
            MeasureLateralCanthalTilt(),
            MeasureFacialWHRatio(),
            MeasureJawFrontalAngle(),
            MeasureCheekBoneHeight(),
            MeasureTotalFacialWHRatio(),
            MeasureBigonialWidth(),
            MeasureChinPhiltrumRatio(),
            MeasureNeckWidth(),
            MeasureMouthNoseWidthRatio(),
            MeasureMidfaceRatio(),
            MeasureEyebrowPositionRatio(),
            MeasureEyeSpacingRatio(),
            MeasureEyeAspectRatio(),
            MeasureLowerUpperLipRatio(),
            MeasureDeviationOfIaaJfa(),
            MeasureEyebrowTilt(),
            MeasureBitemporalWidth(),
            MeasureLowerThirdProportion(),
            MeasureIpsilateralAlarAngle(),
            MeasureMedialCanthalAngle(),
            
            MeasureGonialAngle(),
            MeasureNasofrontalAngle(),
            MeasureMandibularPlaneAngle(),
            MeasureRamusMandibleRatio(),
            MeasureFacialConvexityGlabella(),
            MeasureSubmentalCervicalAngle(),
            MeasureNasoFacialAngle(),
            MeasureNasoLabialAngle(),
            MeasureOrbitalVector(),
            MeasureTotalFacialConvexity(),
            MeasureMentolabialAngle(),
            MeasureFacialConvexityNasion(),
            MeasureNasalProjection(),
            MeasureNasalWHRatio(),
            MeasureRickettsELine(),
            MeasureHoldawayHLine(),
            MeasureSteinerSLine(),
            MeasureBurstoneLine(),
            MeasureNasomentalAngle(),
            MeasureGonionMouthRelationship(),
            MeasureRecessionRelativeFrankfortPlane(),
            MeasureBrowridgeInclinationAngle(),
            MeasureNasalTipAngle(),            
        ]
       
        for index in range (len(self.measures)):
            self.measures[index].race = race
            self.measures[index].gender = gender
            self.measures[index].name = features[index]
            self.measures[index].points = points
            self.measures[index].lines = lines

    def get_values(self):
        res = []
        for measure in self.measures:
            measure.calc()
            res.append(measure.get())

        return res