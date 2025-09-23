from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta

from . import models, schemas, database

SECRET_KEY = "secret123"  # ganti di production
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/v1", 
                   tags=["auth"])

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(database.SessionLocal)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = bcrypt.hash(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        username=user.username,
        password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_token({"sub": user.email})
    return {"response": {"token": token}}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not bcrypt.verify(user.password, db_user.password):
        return {"message": "Invalid credentials"}

    token = create_token({"sub": user.email})
    return {"response": {"token": token}}
