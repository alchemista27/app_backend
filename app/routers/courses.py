from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/course", tags=["Course"])

@router.get("/", response_model=list[schemas.CourseOut])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/search/{query}", response_model=list[schemas.CourseOut])
def search_course(query: str, db: Session = Depends(get_db)):
    return db.query(models.Course).filter(models.Course.title.ilike(f"%{query}%")).all()
