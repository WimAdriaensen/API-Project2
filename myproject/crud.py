from sqlalchemy.orm import Session
from fastapi import Response, HTTPException
from starlette import status

import auth
import models
import schemas


# ---------------------------------- COURSES --------------------------------------


def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_name(db: Session, it_course: str):
    return db.query(models.Course).filter(models.Course.name_course == it_course).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(name_course=course.name_course)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course_and_lessons(db: Session, course_id: int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id)
    db_course.delete(synchronize_session=False)
    db_lesson = db.query(models.Lesson).filter(models.Lesson.course_id == course_id)
    db_lesson.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_200_OK, content="Course and its lessons are deleted")


# ---------------------------------- LESSONS --------------------------------------


def get_lesson_by_id(db: Session, lesson_id: int):
    return db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()


def get_lessons_by_course_id(db: Session, course_id: int):
    return db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()


def get_lessons_by_lecturer_id(db: Session, lecturer_id: int):
    return db.query(models.Lesson).filter(models.Lesson.lecturer_id == lecturer_id).all()


def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lesson).offset(skip).limit(limit).all()


def create_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def update_lesson(db: Session, lesson: schemas.LessonPut, lesson_id: int):
    db_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id)
    db_lesson.update(lesson.dict(exclude_unset=True), synchronize_session=False)
    updated_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    db.commit()
    return updated_lesson


# ---------------------------------- LECTURERS ------------------------------------

def get_lecturer_by_id(db: Session, lecturer_id):
    return db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()


def get_lecturer_by_name(db: Session, lecturer: str):
    return db.query(models.Lecturer).filter(models.Lecturer.lecturer == lecturer).first()


def get_lecturers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lecturer).offset(skip).limit(limit).all()


def create_lecturer(db: Session, lecturer: schemas.LecturerCreate):
    db_lecturer = models.Lecturer(lecturer=lecturer.lecturer)
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer


def delete_lecturer_and_lessons(db: Session, lecturer_id: int):
    db_lecturer = db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id)
    db_lecturer.delete(synchronize_session=False)
    db_lesson = db.query(models.Lesson).filter(models.Lesson.lecturer_id == lecturer_id)
    db_lesson.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_200_OK, content="Lecturer and its lessons are deleted")



# ------------------------------------- USERS --------------------------------------

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
