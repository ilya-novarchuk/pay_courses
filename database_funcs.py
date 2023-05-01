

from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from database_core import *


# # #
# # # COURSE MANAGMENT
# # #


def create_course(description: str):
    with Session(autoflush=True, bind=engine) as session:
        course = Course(description=description)
        session.add(course)
        session.commit()


def edit_course(id: int, description: str):
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == id).first()
        assert course is not None, 'Course is not exists'
        course.description = description
        session.commit()


def delete_course(id: int):
    with Session(autoflush=True, bind=engine) as session:
        lessons = session.query(Lesson).filter(Lesson.course_id == id)
        for l in lessons:
            session.delete(l)
        course = session.query(Course).filter(Course.id == id).first()
        session.delete(course)
        session.commit()


def get_courses() -> List[Course]:
    with Session(autoflush=True, bind=engine) as session:
        return session.query(Course).all()


def get_course_description(id: int) -> str:
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == id).all()
        assert len(course) == 1, 'Курс не существует'
        return course[0].description


def course_exist(id: int) -> bool:
    with Session(autoflush=True, bind=engine) as session:
        cources = session.query(Course).filter(Course.id == id).all()
        assert len(cources) == 0 or len(cources) == 1
        return len(cources) == 1


# # #
# # # COURSE MANAGMENT END
# # #


# # #
# # # LESSON MANAGMENT
# # #


def create_lesson(course_id: int,
                  description: str,
                  date: datetime):
    with Session(autoflush=True, bind=engine) as session:
        lesson = Lesson(
            course_id=course_id,
            description=description,
            date=date
        )
        session.add(lesson)
        session.commit()


def edit_lesson(id: int,
                new_description: str,
                new_date: datetime):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        lesson.description = new_description
        lesson.date = new_date
        session.commit()


def delete_lesson(id: int):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        session.delete(lesson)
        session.commit()


def get_lessons() -> List[Lesson]:
    with Session(autoflush=True, bind=engine) as session:
        return session.query(Lesson).all()


def get_lessons_by_course(course_id: int) -> List[Lesson]:
    with Session(autoflush=True, bind=engine) as session:
        return session.query(Lesson).filter(Lesson.course_id == course_id).all()


def lesson_exist(id: int) -> bool:
    with Session(autoflush=True, bind=engine) as session:
        lessons = session.query(Lesson).filter(Lesson.id == id).all()
        assert len(lessons) == 0 or len(lessons) == 1
        return len(lessons) == 1


# # #
# # # LESSON MANAGMENT END
# # #
