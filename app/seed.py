from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app import models
from passlib.context import CryptContext
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # --- Categories ---
    categories = [
        models.Category(name="Web Development"),
        models.Category(name="Data Science"),
        models.Category(name="Mobile App"),
        models.Category(name="UI/UX Design"),
    ]
    db.add_all(categories)
    db.commit()

    # --- Users ---
    users = [
        models.User(
            email="alice@example.com",
            password=pwd_context.hash("password123"),
            full_name="Alice Wonderland",
            specialization_id=1,
        ),
        models.User(
            email="bob@example.com",
            password=pwd_context.hash("password123"),
            full_name="Bob Builder",
            specialization_id=2,
        ),
    ]
    db.add_all(users)
    db.commit()

    # --- Courses ---
    courses = [
        models.Course(
            name="Intro to Python",
            description="Learn Python from scratch",
            category_id=2,
            created_at=datetime.datetime.utcnow(),
        ),
        models.Course(
            title="Flutter Mobile Development",
            description="Build apps with Flutter",
            category_id=3,
            created_at=datetime.datetime.utcnow(),
        ),
    ]
    db.add_all(courses)
    db.commit()

    # --- Enrolled Courses ---
    enrolled_courses = [
        models.EnrolledCourse(user_id=1, course_id=1, progress=0),
        models.EnrolledCourse(user_id=2, course_id=2, progress=0),
    ]
    db.add_all(enrolled_courses)
    db.commit()

    # --- FAQ ---
    faqs = [
        models.FAQ(question="How to enroll?", answer="Click enroll button on course page."),
        models.FAQ(question="Can I get certificate?", answer="Yes, after completing course."),
    ]
    db.add_all(faqs)
    db.commit()

    db.close()
    print("Dummy data seeded successfully!")

if __name__ == "__main__":
    seed_data()
