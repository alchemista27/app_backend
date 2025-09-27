from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, user, course, category, faq, download

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Edutiv Backend")

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(category.router)
app.include_router(faq.router)
app.include_router(download.router)
