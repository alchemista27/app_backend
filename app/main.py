from fastapi import FastAPI
from routers import auth, user, course, category, faq, download
from database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Edutiv API", version="1.0.0")

# Register Routers
app.include_router(auth.router, prefix="/user", tags=["Auth & User"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(course.router, prefix="/course", tags=["Course"])
app.include_router(category.router, prefix="/category", tags=["Category"])
app.include_router(faq.router, prefix="/faq", tags=["FAQ"])
app.include_router(download.router, prefix="/enrolled", tags=["Download"])
