

from dataclasses import dataclass
from typing import List

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import UniqueConstraint

import telebot

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
    name = Column(String, unique=True)
    description = Column(String)
    price = Column(Integer)


class Lesson(Base):
    __tablename__ = 'Lessons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('Courses.id'))
    name = Column(String)
    description = Column(String)
    price = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('course_id', 'name', name='_uniq'),
    )


class ShoppingCart(Base):
    __tablename__ = 'ShopingCart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    lesson_id = Column(Integer, ForeignKey('Lessons.id'))

    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='_uniqqq'),
    )


@dataclass
class PayAssigment:
    lesson_ids: List[str]
    prices: List[telebot.types.LabeledPrice]


class TempPayment(Base):
    __tablename__ = 'TempPayments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    lessons = Column(String) # list of lesson id (json)


class LessonAccess(Base):
    __tablename__ = 'LessonAccess'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    lesson_id = Column(Integer, ForeignKey('Lessons.id'))

    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='_uniqqqq'),
    )


Base.metadata.create_all(engine)
