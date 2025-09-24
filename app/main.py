from fastapi import FastAPI
from . import models, database
from .auth import router as auth_router
from .courses import router as course_router
from .topics import router as topic_router
from .lessons import router as lesson_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="PJBLMS API", version="1.0")

app.include_router(auth_router)
app.include_router(course_router)
app.include_router(topic_router)
app.include_router(lesson_router)
