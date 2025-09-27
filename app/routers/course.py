from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/course", tags=["course"])


@router.get("/", response_model=list[schemas.CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/enrolled")
def enroll_course(
    enrollment: schemas.EnrollRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_enroll = models.EnrolledCourse(
        user_id=current_user.id, course_id=enrollment.course_id
    )
    db.add(new_enroll)
    db.commit()
    db.refresh(new_enroll)
    return {"message": "Enrolled successfully"}


@router.put("/enrolled/{enrolled_id}", response_model=schemas.ReviewResponse)
def create_review(
    enrolled_id: int,
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    enrolled = (
        db.query(models.EnrolledCourse)
        .filter(
            models.EnrolledCourse.id == enrolled_id,
            models.EnrolledCourse.user_id == current_user.id,
        )
        .first()
    )
    if not enrolled:
        raise HTTPException(status_code=404, detail="Enrolled course not found")

    enrolled.rating = review.rating
    enrolled.review = review.review
    db.commit()
    db.refresh(enrolled)
    return enrolled


@router.get("/search/{query}", response_model=list[schemas.CourseResponse])
def search_course(query: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Course)
        .filter(models.Course.title.ilike(f"%{query}%"))
        .all()
    )


@router.get("/enrolled/courses/{course_id}", response_model=list[schemas.ReviewResponse])
def reviews_from_course(course_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.EnrolledCourse)
        .filter(models.EnrolledCourse.course_id == course_id)
        .all()
    )


@router.put("/enrolled/progress/{enrolled_id}", response_model=schemas.EnrolledCourseResponse)
def update_progress(
    enrolled_id: int,
    progress: schemas.ProgressUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    enrolled = (
        db.query(models.EnrolledCourse)
        .filter(
            models.EnrolledCourse.id == enrolled_id,
            models.EnrolledCourse.user_id == current_user.id,
        )
        .first()
    )
    if not enrolled:
        raise HTTPException(status_code=404, detail="Enrolled course not found")

    enrolled.material_id = progress.material_id
    db.commit()
    db.refresh(enrolled)
    return enrolled
