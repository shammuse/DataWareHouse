from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class DetectionResultBase(BaseModel):
    image_name: str
    confidence_score: float
    class_name: str
    bbox_coordinates: str 
    result_image_path: str
    detection_time: datetime

class DetectionResultCreate(DetectionResultBase):
    pass

class DetectionResult(DetectionResultBase):
    id: uuid.UUID  # Use UUID type for the ID field

    class Config:
        orm_mode = True
