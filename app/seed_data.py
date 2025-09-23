from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Hapus tabel lama dan buat baru
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# ====== Data Dummy ======
courses_data = [
    {
        "title": "Mastering Entrepreneurship",
        "thumbnail": "https://interactivecares-courses.com/wp-content/uploads/2023/07/Course-Cover-Eng-1024x536.png",
        "sale_price": 2000,
        "regular_price": 1000,
        "author": "PJBLMS UNIB",
        "rating": 5,
        "promo_video": "http://5.231.31.30:8001/media/flutter.mp4",
        "topics": [
            {
                "title": "Module 01: Introduction",
                "total_duration": "00:25:30",
                "total_lesson": 2,
                "lessons": [
                    {
                        "title": "Introduction to entrepreneurship",
                        "lesson_url": "http://5.231.31.30:8001/media/flutter.mp4",
                        "duration": "00:06:53",
                        "is_complete": False
                    },
                    {
                        "title": "Things you need to start a business",
                        "lesson_url": "http://5.231.31.30:8001/media/seo.mp4",
                        "duration": "00:05:29",
                        "is_complete": False
                    }
                ]
            },
            {
                "title": "Module 02: Business Plan",
                "total_duration": "00:06:35",
                "total_lesson": 1,
                "lessons": [
                    {
                        "title": "Business Outline",
                        "lesson_url": "http://5.231.31.30:8001/media/flutter.mp4",
                        "duration": "00:06:35",
                        "is_complete": False
                    }
                ]
            }
        ]
    },
    {
        "title": "DevOps Career Path",
        "thumbnail": "https://interactivecares-courses.com/wp-content/uploads/2023/07/DevOPS-For-Website1-1024x536.png",
        "sale_price": None,
        "regular_price": 12500,
        "author": "PJBLMS UNIB",
        "rating": 4,
        "promo_video": "http://5.231.31.30:8001/media/seo.mp4",
        "topics": [
            {
                "title": "Module 01: Version Control System (VCS)",
                "total_duration": "00:12:09",
                "total_lesson": 2,
                "lessons": [
                    {
                        "title": "Introduction to GIT",
                        "lesson_url": "http://5.231.31.30:8001/media/seo.mp4",
                        "duration": "00:05:25",
                        "is_complete": False
                    },
                    {
                        "title": "Installation and configuration",
                        "lesson_url": "http://5.231.31.30:8001/media/flutter.mp4",
                        "duration": "00:06:43",
                        "is_complete": False
                    }
                ]
            }
        ]
    }
]

# ====== Insert Data ke DB ======
for c in courses_data:
    course = models.Course(
        title=c["title"],
        thumbnail=c["thumbnail"],
        sale_price=c["sale_price"],
        regular_price=c["regular_price"],
        author=c["author"],
        rating=c["rating"],
        promo_video=c["promo_video"]
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    for t in c["topics"]:
        topic = models.Topic(
            title=t["title"],
            total_duration=t["total_duration"],
            total_lesson=t["total_lesson"],
            course_id=course.id
        )
        db.add(topic)
        db.commit()
        db.refresh(topic)

        for l in t["lessons"]:
            lesson = models.Lesson(
                title=l["title"],
                lesson_url=l["lesson_url"],
                duration=l["duration"],
                is_complete=l["is_complete"],
                topic_id=topic.id
            )
            db.add(lesson)
            db.commit()

db.close()
print("✅ Database sudah diisi data dummy courses, topics, dan lessons!")
