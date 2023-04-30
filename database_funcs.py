

from typing import List

from sqlalchemy.orm import Session

from database_core import *


def create_course(description: str):
    with Session(autoflush=True, bind=engine) as session:
        cource = Cource(description=description)
        session.add(cource)
        session.commit()


def get_cources() -> List[Cource]:
    with Session(autoflush=True, bind=engine) as session:
        return session.query(Cource).all()


def edit_course(id: int, description: str):
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Cource).filter(Cource.id == id).first()
        assert course is not None, 'Course is not exists'
        course.description = description
        session.commit()


def delete_course(id: int):
    with Session(autoflush=True, bind=engine) as session:
        lessons = session.query(Lesson).filter(Lesson.cource_id == id)
        for l in lessons:
            session.delete(l)
        course = session.query(Cource).filter(Cource.id == id).first()
        session.delete(course)
        session.commit()
