from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, models, schemas

SECRET_KEY = "secret123"  # ganti di production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/api/v1", 
                   tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
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
