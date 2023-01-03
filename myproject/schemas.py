from pydantic import BaseModel


class CourseBase(BaseModel):
    name_course: str


class LessonBase(BaseModel):
    it_class: str


class LecturerBase(BaseModel):
    lecturer: str


class CourseCreate(CourseBase):
    pass


class LessonCreate(LessonBase):
    pass


class LecturerCreate(LecturerBase):
    pass


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

