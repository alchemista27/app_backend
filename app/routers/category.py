from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/", response_model=list[schemas.CategoryResponse])
def get_all_category(db: Session = Depends(get_db)):
    return db.query(models.Category).all()
