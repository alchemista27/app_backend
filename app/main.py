from fastapi import FastAPI
from . import models, database, auth, courses

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(courses.router)