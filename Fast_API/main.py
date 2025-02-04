import sys
sys.path.append('../')
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from FAST_API import crud, models, schemas
from database import SessionLocal, engine

# Initialize FastAPI
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/detection_results/", response_model=schemas.DetectionResult)
def create_detection_result(result: schemas.DetectionResultCreate, db: Session = Depends(get_db)):
    return crud.create_detection_result(db=db, result=result)

@app.get("/detection_results/", response_model=list[schemas.DetectionResult])
def read_detection_results(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    results = crud.get_detection_results(db, skip=skip, limit=limit)
    return results

@app.get("/detection_results/{result_id}", response_model=schemas.DetectionResult)
def read_detection_result(result_id: int, db: Session = Depends(get_db)):
    db_result = crud.get_detection_result(db, result_id=result_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return db_result

@app.delete("/detection_results/{result_id}")
def delete_detection_result(result_id: int, db: Session = Depends(get_db)):
    db_result = crud.delete_detection_result(db, result_id=result_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return {"message": "Detection result deleted"}
