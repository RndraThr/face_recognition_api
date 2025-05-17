from pydantic import BaseModel
from typing import List
from datetime import datetime

class FaceOut(BaseModel):
    id: int
    name: str
    embedding: List[float]
    created_at: datetime

    class Config:
        from_attributes = True  # supaya bisa langsung parsing dari ORM


class FaceRegisterRequest(BaseModel):
    name: str  # nama orang yang mau diregister


class FaceRecognitionResponse(BaseModel):
    matched: bool  # true kalau wajah ketemu di database
    similarity: float  # seberapa dari rentang (0–1)
    matched_face: FaceOut | None  # data wajah yang paling mirip (kalau ada)
