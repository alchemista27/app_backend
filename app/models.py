from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    thumbnail = Column(String)
    sale_price = Column(Integer, nullable=True)
    regular_price = Column(Integer)
    author = Column(String)
    rating = Column(Integer, nullable=True)
    promo_video = Column(String)
    topics = relationship("Topic", back_populates="course")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    total_duration = Column(String)
    total_lesson = Column(Integer)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="topics")
    lessons = relationship("Lesson", back_populates="topic")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    lesson_url = Column(String)
    duration = Column(String)
    is_complete = Column(Boolean, default=False)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    topic = relationship("Topic", back_populates="lessons")
