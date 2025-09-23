from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

router = APIRouter(prefix="/api/v1", tags=["courses"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.CourseSchema])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

@router.get("/{course_id}", response_model=schemas.CourseSchema)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        return {"error": "Course not found"}
    return course
