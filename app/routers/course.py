from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/course", tags=["course"])

# Fetch all courses
@router.get("/", response_model=list[schemas.CourseResponse])
def fetch_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

# Fetch course by ID
@router.get("/{course_id}", response_model=schemas.CourseResponse)
def fetch_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Enroll user in course
@router.post("/enroll")
def enroll_course(user_id: int, course_id: int, db: Session = Depends(get_db)):
    enrolled = models.EnrolledCourse(user_id=user_id, course_id=course_id, progress=0)
    db.add(enrolled)
    db.commit()
    db.refresh(enrolled)
    return {"message": "User enrolled successfully", "enrolled_course_id": enrolled.id}

# Update course progress
@router.put("/progress/{enrolled_course_id}", response_model=schemas.EnrolledCourseResponse)
def update_progress(enrolled_course_id: int, material_id: int, db: Session = Depends(get_db)):
    enrolled = db.query(models.EnrolledCourse).filter(models.EnrolledCourse.id == enrolled_course_id).first()
    if not enrolled:
        raise HTTPException(status_code=404, detail="Enrolled course not found")
    enrolled.progress = material_id
    db.commit()
    db.refresh(enrolled)
    return enrolled
