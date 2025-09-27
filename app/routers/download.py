from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import os

router = APIRouter(prefix="/enrolled", tags=["download"])

# Download certificate/report for enrolled course
@router.get("/download-report/{enrolled_course_id}")
def download_report(enrolled_course_id: int, db: Session = Depends(get_db)):
    enrolled = db.query(models.EnrolledCourse).filter(models.EnrolledCourse.id == enrolled_course_id).first()
    if not enrolled:
        raise HTTPException(status_code=404, detail="Enrolled course not found")
    # Simulate file path
    file_path = f"./files/certificate_{enrolled_course_id}.pdf"
    if not os.path.exists(file_path):
        # Create dummy file if not exists
        with open(file_path, "wb") as f:
            f.write(b"Dummy certificate PDF content")
    return FileResponse(path=file_path, media_type='application/pdf', filename=f"certificate_{enrolled_course_id}.pdf")
