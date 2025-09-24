from pydantic import BaseModel
from typing import List, Optional

class LessonSchema(BaseModel):
    title: str
    lessonUrl: str
    duration: str
    isComplete: bool

    class Config:
        orm_mode = True

class TopicSchema(BaseModel):
    title: str
    totalDuration: str
    totalLesson: int
    lesson: Optional[List[LessonSchema]] = []

    class Config:
        orm_mode = True

class CourseSchema(BaseModel):
    title: str
    thumbnail: str
    salePrice: Optional[int]
    regularPrice: int
    author: str
    rating: Optional[int]
    topics: Optional[List[TopicSchema]] = []
    promoVide: str

    class Config:
        orm_mode = True

class UserRegister(BaseModel):
    full_name: str
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class LessonProgressSchema(BaseModel):
    user_id: int
    lesson_id: int
    is_complete: bool

    class Config:
        orm_mode = True

class CourseProgressSummary(BaseModel):
    course_id: int
    course_title: str
    total_lessons: int
    completed_lessons: int
    progress_percentage: float
