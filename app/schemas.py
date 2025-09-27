from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# User
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    specialization_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Course
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Category
class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# FAQ
class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True

# EnrolledCourse
class EnrolledCourseResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
