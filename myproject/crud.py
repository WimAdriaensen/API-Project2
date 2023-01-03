from sqlalchemy.orm import Session

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


# ---------------------------------- LESSONS --------------------------------------


def get_lesson_by_id(db: Session, lesson_id: int):
    return db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()


def get_lessons_by_course_id(db: Session, course_id: int):
    return db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()


def get_lessons_by_lecturer_id(db: Session, lecturer_id: int):
    return db.query(models.Lesson).filter(models.Lesson.lecturer_id == lecturer_id).all()


def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lesson).offset(skip).limit(limit).all()


def create_lesson(db: Session, lesson: schemas.LessonCreate, course_id: int, lecturer_id: int):
    db_lesson = models.Lesson(**lesson.dict(), course_id=course_id, lecturer_id=lecturer_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


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
