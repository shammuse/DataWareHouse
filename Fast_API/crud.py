from sqlalchemy.orm import Session
import uuid
from . import models, schemas

def get_detection_result(db: Session, result_id:uuid.UUID):
    result = db.query(models.DetectionResult).filter(models.DetectionResult.id == result_id).first()
    if result:
        print(f"Found detection result: {result}")
    else:
        print(f"No detection result found with id: {result_id}")
    return result

def get_detection_results(db: Session, skip: int = 0, limit: int = 10):
    results = db.query(models.DetectionResult).offset(skip).limit(limit).all()
    print(f"Returning {len(results)} results")  # Add logging for troubleshooting
    return results

def create_detection_result(db: Session, result: schemas.DetectionResultCreate):
    db_result = models.DetectionResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    print(f"Created detection result: {db_result}")  # Add logging for troubleshooting
    return db_result


def delete_detection_result(db: Session, result_id:uuid.UUID):
    db_result = get_detection_result(db, result_id)
    if db_result:
        db.delete(db_result)
        db.commit()
        return db_result
    return None
