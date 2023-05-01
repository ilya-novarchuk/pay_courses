

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

import config


engine = sqlalchemy.create_engine(config.DATABASE, echo=True)
Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)


class Course(Base):
    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)


class Lesson(Base):
    __tablename__ = 'Lessons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('Courses.id'))
    description = Column(String)
    date = Column(DateTime, nullable=False)


class Payment(Base):
    __tablename__ = 'Payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    lesson_id = Column(Integer, ForeignKey('Lessons.id'))



Base.metadata.create_all(engine)
