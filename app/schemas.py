from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    full_name: str
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CourseBase(BaseModel):
    title: str
    description: str

class CourseOut(CourseBase):
    id: int
    class Config:
        orm_mode = True

class MaterialOut(BaseModel):
    id: int
    title: str
    content: str
    class Config:
        orm_mode = True

class EnrollRequest(BaseModel):
    user_id: int
    course_id: int

class ReviewRequest(BaseModel):
    rating: int
    review: str

class ProgressRequest(BaseModel):
    material_id: int