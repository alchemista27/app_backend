from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.dependencies import get_current_user
import os

router = APIRouter(prefix="/enrolled", tags=["download"])


@router.get("/download-report/{enrolled_id}")
def download_report(
    enrolled_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    enrolled = (
        db.query(models.EnrolledCourse)
        .filter(
            models.EnrolledCourse.id == enrolled_id,
            models.EnrolledCourse.user_id == current_user.id,
        )
        .first()
    )
    if not enrolled:
        raise HTTPException(status_code=404, detail="Enrolled course not found")

    # misalnya report PDF disimpan di folder reports/{enrolled_id}.pdf
    file_path = f"reports/{enrolled_id}.pdf"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(path=file_path, filename=f"report_{enrolled_id}.pdf")
