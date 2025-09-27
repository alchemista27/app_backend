from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hashed password

    enrolled_courses = relationship("EnrolledCourse", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)

    materials = relationship("Material", back_populates="course")
    enrolled_courses = relationship("EnrolledCourse", back_populates="course")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="materials")

class EnrolledCourse(Base):
    __tablename__ = "enrolled_courses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    rating = Column(Integer, nullable=True)
    review = Column(Text, nullable=True)

    user = relationship("User", back_populates="enrolled_courses")
    course = relationship("Course", back_populates="enrolled_courses")
    progresses = relationship("Progress", back_populates="enrolled_course")

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    enrolled_course_id = Column(Integer, ForeignKey("enrolled_courses.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    completed_at = Column(DateTime, default=func.now())

    enrolled_course = relationship("EnrolledCourse", back_populates="progresses")