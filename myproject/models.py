from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name_course = Column(String, index=True)

    lessons = relationship("Lesson", back_populates="course")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    it_class = Column(String, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    lecturer_id = Column(Integer, ForeignKey("lecturers.id"))

    course = relationship("Course", back_populates="lessons")
    lecturer = relationship("Lecturer", back_populates="lessons")


class Lecturer(Base):
    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)
    lecturer = Column(String, index=True)

    lessons = relationship("Lesson", back_populates="lecturer")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
