import time

import requests
import json


# ------------------- TEST GET - REQUESTS -----------------------
def test_get_courses():
    response = requests.get('http://127.0.0.1:8000/courses')
    assert response.status_code == 200


def test_get_courses_with_id():
    response = requests.get('http://127.0.0.1:8000/courses/1')
    assert response.status_code == 200
    response_dict = response.json()
    assert type(response_dict["name_course"]) == str
    assert type(response_dict["lessons"]) == list


def test_get_courses_with_wrong_id():
    response = requests.get('http://127.0.0.1:8000/courses/999')
    assert response.status_code == 404
    response_dict = response.json()
    assert response_dict["detail"] == 'Course not found'


def test_get_courses_with_string():
    response = requests.get('http://127.0.0.1:8000/courses/java')
    assert response.status_code == 422


def test_get_lecturers():
    response = requests.get('http://127.0.0.1:8000/lecturers')
    assert response.status_code == 200


def test_get_lecturers_with_id():
    response = requests.get('http://127.0.0.1:8000/lecturers/1')
    assert response.status_code == 200
    response_dict = response.json()
    assert type(response_dict["lecturer"]) == str
    assert type(response_dict["lessons"]) == list


def test_get_lecturers_with_wrong_id():
    response = requests.get('http://127.0.0.1:8000/lecturers/999')
    assert response.status_code == 404
    response_dict = response.json()
    assert response_dict["detail"] == 'Lecturer not found'


def test_get_lecturers_with_string():
    response = requests.get('http://127.0.0.1:8000/lecturers/Michiel')
    assert response.status_code == 422


def test_get_lessons():
    response = requests.get('http://127.0.0.1:8000/lessons')
    assert response.status_code == 200


def test_get_lessons_with_id():
    response = requests.get('http://127.0.0.1:8000/lessons/1')
    assert response.status_code == 200
    response_dict = response.json()
    assert type(response_dict["it_class"]) == str
    assert type(response_dict["course_id"]) == int
    assert type(response_dict["lecturer_id"]) == int


def test_get_lessons_with_wrong_id():
    response = requests.get('http://127.0.0.1:8000/lessons/999')
    assert response.status_code == 404
    response_dict = response.json()
    assert response_dict["detail"] == 'Lesson not found'


def test_get_lessons_with_string():
    response = requests.get('http://127.0.0.1:8000/lessons/tweede')
    assert response.status_code == 422


# ------------------- TEST POST - REQUESTS -----------------------

def test_post_course():
    db_course = {'name_course': 'test_course'}
    response = requests.post('http://127.0.0.1:8000/courses', data=json.dumps(db_course))
    response_dict = response.json()
    assert response.status_code == 200
    assert type(response_dict["name_course"]) == str
    assert type(response_dict["lessons"]) == list


def test_post_lecturer():
    db_lecturer = {'lecturer': 'test_lecturer'}
    response = requests.post('http://127.0.0.1:8000/lecturers', data=json.dumps(db_lecturer))
    response_dict = response.json()
    assert response.status_code == 200
    assert type(response_dict["lecturer"]) == str
    assert type(response_dict["lessons"]) == list


def test_post_lesson():
    response1 = requests.get('http://127.0.0.1:8000/courses')
    course_id = len(response1.json())
    response2 = requests.get('http://127.0.0.1:8000/lecturers')
    lecturer_id = len(response2.json())
    db_lesson = {
        'it_class': 'TEST',
        'course_id': course_id,
        'lecturer_id': lecturer_id
    }
    response3 = requests.post('http://127.0.0.1:8000/lessons', data=json.dumps(db_lesson))
    response_dict = response3.json()
    assert response3.status_code == 200
    assert type(response_dict["it_class"]) == str
    assert type(response_dict["course_id"]) == int
    assert type(response_dict["lecturer_id"]) == int


# ------------------- TEST PUT - REQUESTS -----------------------

def test_put_lesson():
    response1 = requests.get('http://127.0.0.1:8000/lessons')
    lesson_id = len(response1.json())
    response2 = requests.get('http://127.0.0.1:8000/courses')
    course_id = len(response2.json())
    response3 = requests.get('http://127.0.0.1:8000/lecturers')
    lecturer_id = len(response3.json())
    url = 'http://127.0.0.1:8000/updlesson/' + str(lesson_id)
    new_lesson = {
        'it_class': 'new_lesson_test',
        'course_id': course_id,
        'lecturer_id': lecturer_id
    }
    response4 = requests.put(url, data=json.dumps(new_lesson))
    response_dict = response4.json()
    assert response4.status_code == 200
    assert response_dict["it_class"] == 'new_lesson_test'


# ------------------- TEST DELETE - REQUESTS -----------------------

def test_delete_course():
    response1 = requests.get('http://127.0.0.1:8000/courses')
    delete_id = len(response1.json())
    url = 'http://127.0.0.1:8000/delcourse/' + str(delete_id)
    response2 = requests.delete(url)
    assert response2.status_code == 200
    assert response2.content == b'Course and its lessons are deleted'


def test_delete_course_wrong_id():
    url = 'http://127.0.0.1:8000/delcourse/999'
    response = requests.delete(url)
    response_dict = response.json()
    assert response.status_code == 404
    assert response_dict["detail"] == "Course not found"


def test_delete_course_with_string():
    url = 'http://127.0.0.1:8000/delcourse/java'
    response = requests.delete(url)
    assert response.status_code == 422


def test_delete_lecturer():
    response1 = requests.get('http://127.0.0.1:8000/lecturers')
    delete_id = len(response1.json())
    url = 'http://127.0.0.1:8000/dellecturer/' + str(delete_id)
    response2 = requests.delete(url)
    assert response2.status_code == 200
    assert response2.content == b'Lecturer and its lessons are deleted'


def test_delete_lecturer_wrong_id():
    url = 'http://127.0.0.1:8000/dellecturer/999'
    response = requests.delete(url)
    response_dict = response.json()
    assert response.status_code == 404
    assert response_dict["detail"] == "Lecturer not found"


def test_delete_lecturer_with_string():
    url = 'http://127.0.0.1:8000/delcourse/Michiel'
    response = requests.delete(url)
    response_dict = response.json()
    assert response.status_code == 422
