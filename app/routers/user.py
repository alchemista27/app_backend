from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
import jwt

router = APIRouter(prefix="/user", tags=["user"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecretkey"

# Fetch all users
@router.get("/", response_model=list[schemas.UserResponse])
def fetch_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Fetch user by id
@router.get("/{user_id}", response_model=schemas.UserResponse)
def fetch_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update profile
@router.put("/edit-user", response_model=schemas.UserResponse)
def update_profile(user_id: int, specialization_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.specialization_id = specialization_id
    db.commit()
    db.refresh(user)
    return user

# Change password
@router.put("/change-password")
def change_password(user_id: int, current_password: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(current_password, user.password):
        raise HTTPException(status_code=400, detail="Current password invalid")
    user.password = pwd_context.hash(new_password)
    db.commit()
    return {"message": "Password changed successfully"}

# Fetch enrolled courses for user
@router.get("/enrolled/history", response_model=list[schemas.EnrolledCourseResponse])
def fetch_enrolled_courses(user_id: int, db: Session = Depends(get_db)):
    enrolled = db.query(models.EnrolledCourse).filter(models.EnrolledCourse.user_id == user_id).all()
    return enrolled
