from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import LoginRequest, TokenResponse, RegisterRequest
from models.user import User
from utils import verify_password, hash_password, create_access_token
from database import get_db

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(payload.password)
    new_user = User(email=payload.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
