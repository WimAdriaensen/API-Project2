from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth

import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()


# -------------CORS----------------------
# origins = [
#     "http://localhost/",
#     "http://localhost:8080/",
#     "https://localhost.tiangolo.com/",
#     "http://127.0.0.1:5500/",
#     "https://wimadriaensen.github.io",
#     "http://localhost:63343"
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# ----------------------------------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    return crud.create_course(db=db, course=course)


@app.get("/courses/", response_model=list[schemas.Course])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@app.get("/courses/{course_id}", response_model=schemas.Course)
def get_course_by_id(course_id: int, db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
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

@app.delete("/delcourse/{course_id}", response_model=schemas.Course)
def delete_course_and_lessons(course_id: int, db: Session = Depends(get_db),
                              token: str = Depends(oauth2_scheme)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_course_and_lessons(db, course_id=course_id)


# ____________________________________________________________________


@app.post("/lessons/", response_model=schemas.Lesson)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    return crud.create_lesson(db, lesson=lesson)


@app.get("/lessons/", response_model=list[schemas.Lesson])
def get_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    lessons = crud.get_lessons(db, skip=skip, limit=limit)
    return lessons


@app.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def get_lesson_by_id(lesson_id: int, db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    db_lesson = crud.get_lesson_by_id(db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson


# "app get lesson by 'lecturer_id' + 'course_id' " nog doen?


@app.put("/updlesson/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(lesson_id: int, lesson: schemas.LessonPut,
                  db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_lesson = crud.get_lesson_by_id(db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return crud.update_lesson(db, lesson=lesson, lesson_id=lesson_id)


# _________________________________________________________________________


@app.post("/lecturers/", response_model=schemas.Lecturer)
def create_lecturer(lecturer: schemas.LecturerCreate, db: Session = Depends(get_db),
                    token: str = Depends(oauth2_scheme)):
    db_lecturer = crud.get_lecturer_by_name(db, lecturer=lecturer.lecturer)
    if db_lecturer:
        raise HTTPException(status_code=400, detail="Lecturer already created")
    return crud.create_lecturer(db, lecturer=lecturer)


@app.get("/lecturers/", response_model=list[schemas.Lecturer])
def get_lecturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    lecturers = crud.get_lecturers(db, skip=skip, limit=limit)
    return lecturers


@app.get("/lecturers/{lecturer_id}", response_model=schemas.Lecturer)
def get_lecturer_by_id(lecturer_id: int, db: Session = Depends(get_db),
                       token: str = Depends(oauth2_scheme)):
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

# _________________________________________________________________________
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# _________________________________________________________________________

@app.get("/users/me", response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.get_current_active_user(db, token)
    return current_user


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}
