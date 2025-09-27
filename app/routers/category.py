from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/category", tags=["category"])

@router.get("/", response_model=list[schemas.CategoryResponse])
def fetch_all_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories
