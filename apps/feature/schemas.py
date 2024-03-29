from pydantic import BaseModel

class FeaturePoints(BaseModel):
    gender: int = 0
    race: int = 0
    points: list[list] = [[]]