from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas

router = APIRouter(prefix="/api/v1/progress", tags=["Progress"])

# --- GET PROGRESS BY USER ---
@router.get("/user/{user_id}", response_model=List[schemas.LessonProgressSchema])
def get_user_progress(user_id: int, db: Session = Depends(database.get_db)):
    progress = db.query(models.LessonProgress).filter(models.LessonProgress.user_id == user_id).all()
    return progress

# --- UPDATE OR CREATE PROGRESS ---
@router.post("/", response_model=schemas.LessonProgressSchema)
def set_progress(data: schemas.LessonProgressSchema, db: Session = Depends(database.get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == data.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    progress = (
        db.query(models.LessonProgress)
        .filter(models.LessonProgress.user_id == data.user_id, models.LessonProgress.lesson_id == data.lesson_id)
        .first()
    )

    if progress:
        progress.is_complete = data.is_complete
    else:
        progress = models.LessonProgress(
            user_id=data.user_id,
            lesson_id=data.lesson_id,
            is_complete=data.is_complete,
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)
    return progress

@router.get("/summary/{user_id}", response_model=List[schemas.CourseProgressSummary])
def get_course_progress_summary(user_id: int, db: Session = Depends(database.get_db)):
    courses = db.query(models.Course).all()
    summaries = []

    for course in courses:
        total_lessons = 0
        completed_lessons = 0

        for topic in course.topics:
            for lesson in topic.lessons:
                total_lessons += 1
                progress = (
                    db.query(models.LessonProgress)
                    .filter(
                        models.LessonProgress.user_id == user_id,
                        models.LessonProgress.lesson_id == lesson.id,
                        models.LessonProgress.is_complete == True
                    )
                    .first()
                )
                if progress:
                    completed_lessons += 1

        progress_percentage = (
            (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        )

        summaries.append(
            schemas.CourseProgressSummary(
                course_id=course.id,
                course_title=course.title,
                total_lessons=total_lessons,
                completed_lessons=completed_lessons,
                progress_percentage=round(progress_percentage, 2)
            )
        )

    return summaries
