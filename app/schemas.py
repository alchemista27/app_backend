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
