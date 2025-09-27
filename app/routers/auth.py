from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext
import jwt, datetime

router = APIRouter(prefix="/user", tags=["user"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecretkey"

def create_access_token(data: dict, expires_delta: int = 60):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

@router.post("/login", response_model=schemas.Token)
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/", response_model=schemas.UserResponse)
def get_logged_in_user(token: str = Depends(lambda: ""), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token.replace("Bearer ", ""), SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
