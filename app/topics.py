from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas

router = APIRouter(prefix="/api/v1/topics", tags=["Topics"])

# --- GET TOPICS BY COURSE ID ---
@router.get("/course/{course_id}", response_model=List[schemas.TopicSchema])
def get_topics(course_id: int, db: Session = Depends(database.get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.topics

# --- CREATE TOPIC ---
@router.post("/course/{course_id}", response_model=schemas.TopicSchema)
def create_topic(course_id: int, topic: schemas.TopicSchema, db: Session = Depends(database.get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_topic = models.Topic(
        title=topic.title,
        total_duration=topic.totalDuration,
        total_lesson=topic.totalLesson,
        course_id=course_id
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

# --- UPDATE TOPIC ---
@router.put("/{topic_id}", response_model=schemas.TopicSchema)
def update_topic(topic_id: int, topic: schemas.TopicSchema, db: Session = Depends(database.get_db)):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db_topic.title = topic.title
    db_topic.total_duration = topic.totalDuration
    db_topic.total_lesson = topic.totalLesson
    db.commit()
    db.refresh(db_topic)
    return db_topic

# --- DELETE TOPIC ---
@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(database.get_db)):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.delete(db_topic)
    db.commit()
    return {"detail": "Topic deleted successfully"}