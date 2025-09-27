from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ---------------------------
# User Schemas
# ---------------------------
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

# ---------------------------
# Course Schemas
# ---------------------------
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ---------------------------
# Category Schemas
# ---------------------------
class CategoryBase(BaseModel):
    name: str

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ---------------------------
# FAQ Schemas
# ---------------------------
class FAQBase(BaseModel):
    question: str
    answer: str

class FAQResponse(FAQBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ---------------------------
# EnrolledCourse Schemas
# ---------------------------
class EnrolledCourseBase(BaseModel):
    user_id: int
    course_id: int
    progress: int = 0

class EnrolledCourseResponse(EnrolledCourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None
    course: Optional[CourseResponse] = None

    class Config:
        orm_mode = True

# ---------------------------
# Token Schema (Auth)
# ---------------------------
class Token(BaseModel):
    access_token: str
    token_type: str
