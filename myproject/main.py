from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Union  # Dit moet ik gebruiken omdat ik anders de "None | Nonen" niet kan gebruiken
# Deze wordt vervangen door "Union[str, None] = None"
import requests
from fastapi.middleware.cors import CORSMiddleware

class Course(BaseModel):
    id: int
    name_course: str
    lecturer: str

app = FastAPI()

origins = [
    "http://localhost/",
    "http://localhost:8080/",
    "https://localhost.tiangolo.com/",
    "http://127.0.0.1:5500/",
    "https://wimadriaensen.github.io",
    "http://127.0.0.1:63343/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




course_api = {
    "id": 1,
    "name_course": "API Development",
    "lecturer": "Michiel Verboven"
}

course_iot = {
    "id": 2,
    "name_course": "IoT Advanced",
    "lecturer": "Stef Van Wolputte"
}

courses_dict = {}
courses_list = []

courses_list.append(course_api)
courses_list.append(course_iot)
courses_dict = courses_list


@app.get("/courses")
async def show_courses():
    return courses_dict


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Optie voor een extra GET? --> https://api.github.com/repos/wimadriaensen/wimadriaensen.github.io
# bv. url van mijn github ophalen
@app.get("/maker")
async def show_maker():
    response = requests.get("https://api.github.com/repos/wimadriaensen/wimadriaensen.github.io")
    response_dict = {}
    response_dict["owner"] = response.json()["owner"]["login"]
    response_dict["github"] = response.json()["owner"]["html_url"]
    response_dict["repository"] = response.json()["html_url"]
    return response_dict

@app.post("/courses")
async def create_course(course: Course):
    courses_list.append(course)
    courses_dict = courses_list
    return course

