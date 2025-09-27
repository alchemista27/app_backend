from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/faq", tags=["faq"])


@router.get("/", response_model=list[schemas.FAQResponse])
def get_all_faq(db: Session = Depends(get_db)):
    return db.query(models.FAQ).all()
