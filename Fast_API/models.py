import uuid
from sqlalchemy import Column, String, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    image_name = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    class_name = Column(String, nullable=False)
    bbox_coordinates = Column(String, nullable=False)
    result_image_path = Column(String, nullable=False)
    detection_time = Column(TIMESTAMP, nullable=False)