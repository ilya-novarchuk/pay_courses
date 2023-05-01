

from datetime import datetime
from typing import List

import sqlalchemy.exc
from sqlalchemy.orm import Session

from database_core import *


# # #
# # # COURSE MANAGMENT
# # #


def create_course(name: str,
                  description: str,
                  price: int):
    with Session(autoflush=True, bind=engine) as session:
        course = Course(
            name=name,
            description=description,
            price=price
        )
        session.add(course)
        session.commit()


def edit_course_name(id: int, new_name: str):
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == id).first()
        assert course is not None, 'Course is not exists'
        course.name = new_name
        session.commit()


def edit_course_description(id: int, new_description: str):
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == id).first()
        assert course is not None, 'Course is not exists'
        course.description = new_description
        session.commit()


def edit_course_price(id: int, new_price: int):
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == id).first()
        assert course is not None, 'Course is not exists'
        course.price = new_price
        session.commit()


def delete_course(id: int):
    with Session(autoflush=True, bind=engine) as session:
        lessons = session.query(Lesson).filter(Lesson.course_id == id)
        for l in lessons:
            session.delete(l)
        course = session.query(Course).filter(Course.id == id).first()
        session.delete(course)
        session.commit()


def get_course_id(name: str) -> int:
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.name == name).first()
        assert course is not None, 'Course is not exists'
        return course.id


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
                  name: str,
                  description: str,
                  price: int,
                  date: datetime):
    with Session(autoflush=True, bind=engine) as session:
        lesson = Lesson(
            course_id=course_id,
            name=name,
            description=description,
            price=price,
            date=date
        )
        session.add(lesson)
        session.commit()


def edit_lesson_name(id: int, new_name: str):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        assert lesson is not None, 'Course is not exists'
        lesson.name = new_name
        session.commit()


def edit_lesson_description(id: int, new_description: str):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        assert lesson is not None, 'Course is not exists'
        lesson.description = new_description
        session.commit()


def edit_lesson_price(id: int, new_price: int):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        assert lesson is not None, 'Course is not exists'
        lesson.price = new_price
        session.commit()


def edit_lesson_date(id: int, new_date: datetime):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        assert lesson is not None, 'Course is not exists'
        lesson.date = new_date
        session.commit()


def delete_lesson(id: int):
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        session.delete(lesson)
        session.commit()


def get_lesson_id(course_id: int,
                  lesson_name: str
                  ) -> int:
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(
            Lesson.course_id == course_id and Lesson.name == lesson_name).first()
        assert lesson is not None, 'Lesson is not exist'
        return lesson.id


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


# # #
# # # USERS MANAGMENT
# # #


def add_user(telegram_id: str):
    with Session(autoflush=True, bind=engine) as session:
        user = User(telegram_id=telegram_id)
        try:
            session.add(user)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass


# # #
# # # USERS MANAGMENT END
# # #
