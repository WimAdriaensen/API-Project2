from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')


models.Base.metadata.create_all(bind=engine)


app: FastAPI = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db:Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)


@app.get("/courses/", response_model=list[schemas.Course])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@app.get("/courses/{course_id}", response_model=schemas.Course)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


# @app.get("/courses/{it_course}", response_model=schemas.Course)
# def get_course_by_name(it_course: str, db: Session = Depends(get_db)):
#     db_course = crud.get_course_by_name(db, it_course=it_course)
#     if db_course is None:
#         raise HTTPException(status_code=404, detail="Course not found")
#     return db_course

# ____________________________________________________________________


@app.post("/lessons/", response_model=schemas.Lesson)
def create_lesson(course_id: int, lecturer_id: int, lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    return crud.create_lesson(db, lesson=lesson, course_id=course_id, lecturer_id=lecturer_id)


@app.get("/lessons/", response_model=list[schemas.Lesson])
def get_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lessons = crud.get_lessons(db, skip=skip, limit=limit)
    return lessons


@app.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def get_lesson_by_id(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = crud.get_lesson_by_id(db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson

# "app get lesson by 'lecturer_id' + 'course_id' " nog doen

# _________________________________________________________________________


@app.post("/lecturers/", response_model=schemas.Lecturer)
def create_lecturer(lecturer: schemas.LecturerCreate, db: Session = Depends(get_db)):
    db_lecturer = crud.get_lecturer_by_name(db, lecturer=lecturer.lecturer)
    if db_lecturer:
        raise HTTPException(status_code=400, detail="Lecturer already created")
    return crud.create_lecturer(db, lecturer=lecturer)


@app.get("/lecturers/", response_model=list[schemas.Lecturer])
def get_lecturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lecturers = crud.get_lecturers(db, skip=skip, limit=limit)
    return lecturers


@app.get("/lecturers/{lecturer_id}", response_model=schemas.Lecturer)
def get_lecturer_by_id(lecturer_id: int, db: Session = Depends(get_db)):
    db_lecturer = crud.get_lecturer_by_id(db, lecturer_id=lecturer_id)
    if db_lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return db_lecturer


# @app.get("/lecturers/{lecturer}", response_model=schemas.Lecturer)
# def get_lecturer_by_name(lecturer: str, db: Session = Depends(get_db)):
#     db_lecturer = crud.get_lecturer_by_name(db, lecturer=lecturer)
#     if db_lecturer is None:
#         raise HTTPException(status_code=404, detail="Lecturer not found")
#     return db_lecturer
