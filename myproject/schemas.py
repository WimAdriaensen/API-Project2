from pydantic import BaseModel


# -----------------BASES-------------
class CourseBase(BaseModel):
    name_course: str


class LessonBase(BaseModel):
    it_class: str


class LecturerBase(BaseModel):
    lecturer: str


# ----------------CREATING-----------
class CourseCreate(CourseBase):
    pass


class LessonCreate(LessonBase):
    course_id: int
    lecturer_id: int


class LecturerCreate(LecturerBase):
    pass


# ----------------FULL-----------
class Lesson(LessonBase):
    id: int
    course_id: int
    lecturer_id: int

    class Config:
        orm_mode = True


class Course(CourseBase):
    id: int
    lessons: list[Lesson] = []

    class Config:
        orm_mode = True


class Lecturer(LecturerBase):
    id: int
    lessons: list[Lesson] = []

    class Config:
        orm_mode = True


# ----------------PUTS-----------
class LessonPut(LessonBase):
    course_id: int
    lecturer_id: int


# ----------------USER CLASSES FOR AUTHENTICATION-----------

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True