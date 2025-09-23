from fastapi import FastAPI
from . import models, database, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth.router)
