from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/edit-user", response_model=schemas.UserResponse)
def update_profile(
    specialization_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.specialization_id = specialization_id
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/change-password", response_model=schemas.UserResponse)
def change_password(
    current_password: str,
    new_password: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Wrong current password")

    current_user.password = pwd_context.hash(new_password)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/enrolled/history", response_model=list[schemas.EnrolledCourseResponse])
def enrolled_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.EnrolledCourse)
        .filter(models.EnrolledCourse.user_id == current_user.id)
        .all()
    )


@router.post("/request", response_model=schemas.RequestResponse)
def create_request(
    req: schemas.RequestCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_req = models.Request(
        user_id=current_user.id,
        title=req.title,
        category_id=req.category_id,
        request_type=req.request_type,
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req
