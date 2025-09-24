from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas

router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])

# --- GET ALL COURSES ---
@router.get("/", response_model=List[schemas.CourseSchema])
def get_courses(db: Session = Depends(database.get_db)):
    return db.query(models.Course).all()

# --- GET COURSE BY ID ---
@router.get("/{course_id}", response_model=schemas.CourseSchema)
def get_course(course_id: int, db: Session = Depends(database.get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# --- CREATE COURSE ---
@router.post("/", response_model=schemas.CourseSchema)
def create_course(course: schemas.CourseSchema, db: Session = Depends(database.get_db)):
    new_course = models.Course(
        title=course.title,
        thumbnail=course.thumbnail,
        sale_price=course.salePrice,
        regular_price=course.regularPrice,
        author=course.author,
        rating=course.rating,
        promo_video=course.promoVide
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# --- DELETE COURSE ---
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(database.get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted successfully"}
