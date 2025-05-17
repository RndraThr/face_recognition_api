from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Float
from sqlalchemy.sql import func
from app.database import Base

class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
