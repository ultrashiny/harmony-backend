from pydantic import BaseModel



class FeaturePoints(BaseModel):
    points : list[list]