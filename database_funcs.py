

import json
from datetime import datetime
from typing import Dict, List

import sqlalchemy.exc
from sqlalchemy.orm import Session

import telebot

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


def get_course_name(course_id: int) -> str:
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == course_id).first()
        assert course is not None, 'Course is not exists'
        return course.name


def get_course_price(course_id: int) -> int:
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == course_id).first()
        assert course is not None, 'Course is not exists'
        return course.price


def get_courses() -> List[Course]:
    with Session(autoflush=True, bind=engine) as session:
        return session.query(Course).all()


def get_course_description(id: int) -> str:
    with Session(autoflush=True, bind=engine) as session:
        course = session.query(Course).filter(Course.id == id).all()
        assert len(course) == 1, 'Курс не существует'
        return course[0].description


def get_course_lessons_count(course_id: int) -> int:
    with Session(autoflush=True, bind=engine) as session:
        lessons = session.query(Lesson).filter(
            Lesson.course_id == course_id
        ).all()
        return len(lessons)


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
        lesson = session.query(Lesson).filter(Lesson.course_id == course_id).filter(Lesson.name == lesson_name).first()
        assert lesson is not None, 'Lesson is not exist'
        return lesson.id


def get_lesson_course(lesson_id: int) -> int:
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(
            Lesson.id == lesson_id).first()
        assert lesson is not None, 'Lesson is not exist'
        return lesson.course_id


def get_lesson_name(lesson_id: int) -> str:
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(
            Lesson.id == lesson_id).first()
        assert lesson is not None, 'Lesson is not exist'
        return lesson.name

def get_lesson_price(lesson_id: int) -> int:
    with Session(autoflush=True, bind=engine) as session:
        lesson = session.query(Lesson).filter(
            Lesson.id == lesson_id).first()
        assert lesson is not None, 'Lesson is not exist'
        return lesson.price


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


def get_user_id(telegram_id: str) -> int:
    with Session(autoflush=True, bind=engine) as session:
        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()
        assert user is not None
        return user.id


# # #
# # # USERS MANAGMENT END
# # #


# # #
# # # SHOPPING CART MANAGMENT
# # #


def add_shopping_cart_lesson(user_id: int, lesson_id: int):
    with Session(autoflush=True, bind=engine) as session:
        try:
            cart_lesson = ShoppingCart(user_id=user_id,
                                       lesson_id=lesson_id)
            session.add(cart_lesson)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass


def add_shopping_cart_course(user_id: int, course_id: int):
    with Session(autoflush=True, bind=engine) as session:
        actual_cart = session.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
        actual_cart_les_ids = [cart.lesson_id for cart in actual_cart]
        lessons = session.query(Lesson).filter(Lesson.course_id == course_id).all()
        for lesson in lessons:
            if lesson.id not in actual_cart_les_ids:
                cart_lesson = ShoppingCart(user_id=user_id,
                                            lesson_id=lesson.id)
                session.add(cart_lesson)
        session.commit()


def clean_shopping_cart(user_id: int):
    with Session(autoflush=True, bind=engine) as session:
        carts = session.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
        for cart in carts:
            session.delete(cart)
        session.commit()


def is_empty_shopping_cart(user_id: int) -> bool:
    with Session(autoflush=True, bind=engine) as session:
        t = session.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id
        ).first()
        return t is None


def delete_payed_cart(user_id: int):
    with Session(autoflush=True, bind=engine) as session:
        carts = session.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
        for cart in carts:
            if session.query(LessonAccess).filter(
                LessonAccess.user_id == user_id and
                LessonAccess.lesson_id == cart.lesson_id
            ).first() is not None:
                session.delete(cart)
        session.commit()

# # #
# # # SHOPPING CART MANAGMENT END
# # #


# # #
# # # PAYMENTS TEMP MANAGMENT
# # #


def build_pay_assigment(user_id: int) -> PayAssigment:
    delete_payed_cart(user_id)
    with Session(autoflush=True, bind=engine) as session:
        carts = session.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
        
        lesson_ids = [cart.lesson_id for cart in carts]
        prices = []

        course_counts: Dict[int, int] = dict()

        for cart in carts:
            course_id = get_lesson_course(cart.lesson_id)
            if course_counts.get(course_id) is None:
                course_counts[course_id] = 1
            else:
                course_counts[course_id] += 1

        for course_id in course_counts.keys():
            if course_counts[course_id] == get_course_lessons_count(course_id):
                prices.append(telebot.types.LabeledPrice(
                    label=f'Курс {get_course_name(course_id)}',
                    amount=get_course_price(course_id) * 100
                ))
                carts = [cart for cart in carts if get_lesson_course(cart.lesson_id) != course_id]

        for cart in carts:
            prices.append(telebot.types.LabeledPrice(
                    label=f'Лекция {get_lesson_name(cart.lesson_id)}',
                    amount=get_lesson_price(cart.lesson_id) * 100
                ))

        return PayAssigment(
            lesson_ids=lesson_ids,
            prices=prices
        )


def create_temp_payment(user_id: int, pay_assigment: PayAssigment) -> int:
    with Session(autoflush=True, bind=engine) as session:
        temp_payment = TempPayment(
            user_id=user_id,
            lessons=json.dumps(pay_assigment.lesson_ids)
        )
        session.add(temp_payment)
        session.commit()
        return temp_payment.id


def on_success_payment(temp_payment_id: int):
    with Session(autoflush=True, bind=engine) as session:
        payment = session.query(TempPayment).filter(TempPayment.id == temp_payment_id).first()
        assert payment is not None
        for lesson_id in json.loads(payment.lessons):
            add_access(payment.user_id, lesson_id)


# # #
# # # PAYMENTS TEMP MANAGMENT END
# # #


def add_access(user_id: int, lesson_id: int):
    with Session(autoflush=True, bind=engine) as session:
        try:
            access = LessonAccess(
                user_id=user_id,
                lesson_id=lesson_id
            )
            session.add(access)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass


def is_access_lesson(user_id: int, lesson_id: int) -> bool:
    pass

