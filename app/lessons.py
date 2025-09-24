from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas

router = APIRouter(prefix="/api/v1/lessons", tags=["Lessons"])

# --- GET LESSONS BY TOPIC ID ---
@router.get("/topic/{topic_id}", response_model=List[schemas.LessonSchema])
def get_lessons(topic_id: int, db: Session = Depends(database.get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic.lessons

# --- CREATE LESSON ---
@router.post("/topic/{topic_id}", response_model=schemas.LessonSchema)
def create_lesson(topic_id: int, lesson: schemas.LessonSchema, db: Session = Depends(database.get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    new_lesson = models.Lesson(
        title=lesson.title,
        lesson_url=lesson.lessonUrl,
        duration=lesson.duration,
        is_complete=lesson.isComplete,
        topic_id=topic_id
    )
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

# --- UPDATE LESSON ---
@router.put("/{lesson_id}", response_model=schemas.LessonSchema)
def update_lesson(lesson_id: int, lesson: schemas.LessonSchema, db: Session = Depends(database.get_db)):
    db_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db_lesson.title = lesson.title
    db_lesson.lesson_url = lesson.lessonUrl
    db_lesson.duration = lesson.duration
    db_lesson.is_complete = lesson.isComplete
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# --- DELETE LESSON ---
@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(database.get_db)):
    db_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(db_lesson)
    db.commit()
    return {"detail": "Lesson deleted successfully"}