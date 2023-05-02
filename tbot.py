

from typing import Callable

import dateparser
import telebot

import config
import database_funcs


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def is_admin(id: int | str) -> bool:
    if not isinstance(id, str):
        id = str(id)
    return id in config.TELEGRAM_ADMINS


class BuildMarkup:

    @staticmethod
    def menu(telegram_id) -> telebot.types.ReplyKeyboardMarkup:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns = []
        if is_admin(telegram_id):
            btns.append(telebot.types.KeyboardButton('/create_course'))
            btns.append(telebot.types.KeyboardButton('/edit_course_name'))
            btns.append(telebot.types.KeyboardButton('/edit_course_description'))
            btns.append(telebot.types.KeyboardButton('/edit_course_price'))
            btns.append(telebot.types.KeyboardButton('/delete_course'))
            btns.append(telebot.types.KeyboardButton('/create_lesson'))
            btns.append(telebot.types.KeyboardButton('/edit_lesson_name'))
            btns.append(telebot.types.KeyboardButton('/edit_lesson_description'))
            btns.append(telebot.types.KeyboardButton('/edit_lesson_price'))
            btns.append(telebot.types.KeyboardButton('/edit_lesson_date'))
            btns.append(telebot.types.KeyboardButton('/delete_lesson'))
        btns.append(telebot.types.KeyboardButton('Обзор курсов'))
        btns.append(telebot.types.KeyboardButton('Обзор лекций'))
        btns.append(telebot.types.KeyboardButton('Приобрести курс'))
        btns.append(telebot.types.KeyboardButton('Приобрести лекцию'))
        user_id = database_funcs.get_user_id(telegram_id)
        if not database_funcs.is_user_access_empty(user_id):
            btns.append(telebot.types.KeyboardButton('Доступные лекции'))
        if not database_funcs.is_empty_shopping_cart(user_id):
            btns.append(telebot.types.KeyboardButton('Оплатить'))
            btns.append(telebot.types.KeyboardButton('Очистить корзину'))
        markup.add(*btns)
        return markup

    @staticmethod
    def select_course() -> telebot.types.ReplyKeyboardMarkup:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        courses = database_funcs.get_courses()
        btns = [telebot.types.KeyboardButton(c.name) for c in courses]
        markup.add(*btns)
        return markup

    @staticmethod
    def select_lesson(course_id: int) -> telebot.types.ReplyKeyboardMarkup:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        lessons = database_funcs.get_lessons_by_course(course_id)
        btns = [telebot.types.KeyboardButton(l.name) for l in lessons]
        markup.add(*btns)
        return markup


class CreateCourse:

    @bot.message_handler(commands=['create_course'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id,
                            'Введите название курса:')
            bot.register_next_step_handler(message, CreateCourse.step2)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message):
        name = message.text
        bot.send_message(message.from_user.id,
                        'Введите описание курса:')
        bot.register_next_step_handler(message, CreateCourse.step3, name)

    @staticmethod
    def step3(message: telebot.types.Message,
              name: str):
        description = message.text
        bot.send_message(message.from_user.id,
                        'Введите цену за весь курс:')
        bot.register_next_step_handler(message, CreateCourse.step4,
                                       name, description)

    @staticmethod
    def step4(message: telebot.types.Message,
              name: str,
              description: str):
        try:
            price = int(message.text)
            database_funcs.create_course(name, description, price)
            bot.send_message(message.from_user.id,
                            'Курс создан.',
                            reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class SelectCourse:

    @staticmethod
    def step1(message: telebot.types.Message,
              callback_func: Callable[[telebot.types.Message, int], None],
              post_message: str | None):
        bot.send_message(message.from_user.id,
                         'Выберите курс:',
                          reply_markup=BuildMarkup.select_course())
        bot.register_next_step_handler(message, SelectCourse.step2, callback_func, post_message)

    @staticmethod
    def step2(message: telebot.types.Message,
              callback_func: Callable[[telebot.types.Message, int], None],
              post_message: str | None):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            if post_message is not None:
                bot.send_message(message.from_user.id,
                                 post_message)
                bot.register_next_step_handler(message, callback_func, course_id)
            else:
                callback_func(message, course_id)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class EditCourseName:

    @bot.message_handler(commands=['edit_course_name'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectCourse.step1(message, EditCourseName.step2, 'Введите новое имя:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              course_id: int):
        try:
            new_name = message.text
            database_funcs.edit_course_name(course_id, new_name)
            bot.send_message(message.from_user.id,
                             'Имя курса обновлено.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class EditCourseDescription:

    @bot.message_handler(commands=['edit_course_description'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectCourse.step1(message, EditCourseDescription.step2, 'Введите новое описание:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              course_id: int):
        try:
            new_description = message.text
            database_funcs.edit_course_description(course_id, new_description)
            bot.send_message(message.from_user.id,
                             'Описание курса обновлено.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class EditCoursePrice:

    @bot.message_handler(commands=['edit_course_price'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectCourse.step1(message, EditCoursePrice.step2, 'Введите новую цену:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              course_id: int):
        try:
            new_price = int(message.text)
            database_funcs.edit_course_price(course_id, new_price)
            bot.send_message(message.from_user.id,
                             'Цена курса обновлена.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class DeleteCourse:

    @bot.message_handler(commands=['delete_course'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectCourse.step1(message, DeleteCourse.step2, None)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              course_id: int):
        try:
            database_funcs.delete_course(course_id)
            bot.send_message(message.from_user.id, 'Курс удален.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class CreateLesson:

    @bot.message_handler(commands=['create_lesson'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id,
                            'Выберите курс:',
                            reply_markup=BuildMarkup.select_course())
            bot.register_next_step_handler(message, CreateLesson.step2)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            bot.send_message(message.from_user.id,
                            'Введите название лекции:')
            bot.register_next_step_handler(message, CreateLesson.step3, course_id)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

    @staticmethod
    def step3(message: telebot.types.Message,
              course_id: int):
        lesson_name = message.text
        bot.send_message(message.from_user.id,
                        'Введите описание лекции:')
        bot.register_next_step_handler(message, CreateLesson.step4,
                                       course_id, lesson_name)

    @staticmethod
    def step4(message: telebot.types.Message,
              course_id: int,
              lesson_name: str):
        lesson_description = message.text
        bot.send_message(message.from_user.id,
                         'Введите цену лекции:')
        bot.register_next_step_handler(message, CreateLesson.step5,
                                       course_id,
                                       lesson_name,
                                       lesson_description)

    @staticmethod
    def step5(message: telebot.types.Message,
              course_id: int,
              lesson_name: str,
              lesson_description: str):
        try:
            price = int(message.text)
            bot.send_message(message.from_user.id,
                             'Введите дату проведения:')
            bot.register_next_step_handler(message, CreateLesson.step6,
                                           course_id,
                                           lesson_name,
                                           lesson_description,
                                           price)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

    @staticmethod
    def step6(message: telebot.types.Message,
              course_id: int,
              lesson_name: str,
              lesson_description: str,
              lesson_price):
        try:
            date = dateparser.parse(message.text)
            database_funcs.create_lesson(
                course_id,
                lesson_name,
                lesson_description,
                lesson_price,
                date
            )
            bot.send_message(message.from_user.id,
                             'Лекция создана.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class SelectLesson:

    @staticmethod
    def step1(message: telebot.types.Message,
              callback_func: Callable[[telebot.types.Message, int | None], None],
              post_message: str):
        bot.send_message(message.from_user.id,
                         'Выберите курс:',
                         reply_markup=BuildMarkup.select_course())
        bot.register_next_step_handler(message, SelectLesson.step2,
                                       callback_func, post_message)

    @staticmethod
    def step2(message: telebot.types.Message,
              callback_func: Callable[[telebot.types.Message, int | None], None],
              post_message: str):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            bot.send_message(message.from_user.id,
                             'Выберите лекцию:',
                             reply_markup=BuildMarkup.select_lesson(course_id))
            bot.register_next_step_handler(message,
                                           SelectLesson.step3,
                                           course_id,
                                           callback_func,
                                           post_message)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

    @staticmethod
    def step3(message: telebot.types.Message,
              course_id: int,
              callback_func: Callable[[telebot.types.Message, int | None], None],
              post_message: str):
        try:
            lesson_name = message.text
            lesson_id = database_funcs.get_lesson_id(course_id, lesson_name)
            if post_message is not None:
                bot.send_message(message.from_user.id, post_message)
                bot.register_next_step_handler(message,
                                               callback_func,
                                               lesson_id)
            else:
                callback_func(message, lesson_id)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class EditLessonName:

    @bot.message_handler(commands=['edit_lesson_name'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectLesson.step1(message, EditLessonName.step2, 'Введите новое название:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              lesson_id: id):
        try:
            new_name = message.text
            database_funcs.edit_lesson_name(lesson_id, new_name)
            bot.send_message(message.from_user.id,
                             'Название лекции обновлено.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class EditLessonDescription:

    @bot.message_handler(commands=['edit_lesson_description'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectLesson.step1(message, EditLessonDescription.step2, 'Введите новое описание:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              lesson_id: id):
        try:
            new_description = message.text
            database_funcs.edit_lesson_description(lesson_id, new_description)
            bot.send_message(message.from_user.id,
                             'Описание лекции обновлено.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

class EditLessonPrice:

    @bot.message_handler(commands=['edit_lesson_price'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectLesson.step1(message, EditLessonPrice.step2, 'Введите новую цену:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              lesson_id: id):
        try:
            new_price = int(message.text)
            database_funcs.edit_lesson_price(lesson_id, new_price)
            bot.send_message(message.from_user.id,
                             'Цена лекции обновлена.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class EditLessonDate:

    @bot.message_handler(commands=['edit_lesson_date'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectLesson.step1(message, EditLessonDate.step2, 'Введите новое время:')
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              lesson_id: id):
        try:
            new_date = dateparser.parse(message.text)
            database_funcs.edit_lesson_date(lesson_id, new_date)
            bot.send_message(message.from_user.id,
                             'Цена лекции обновлена.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class DeleteLesson:

    @bot.message_handler(commands=['delete_lesson'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            SelectLesson.step1(message, DeleteLesson.step2, None)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message,
              lesson_id: id):
        try:
            database_funcs.delete_lesson(lesson_id)
            bot.send_message(message.from_user.id,
                             'Лекция удалена.',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class ViewCourses:

    @bot.message_handler(commands=['view_courses'])
    @staticmethod
    def step1(message: telebot.types.Message):
        courses = database_funcs.get_courses()
        to_text = 'Список доступных курсов:'
        for c in courses:
            to_text += f'\n\n{c.name}\n{c.description}'
        bot.send_message(message.from_user.id, to_text)


class ViewCourse:

    @bot.message_handler(commands=['view_course'])
    @staticmethod
    def step1(message: telebot.types.Message):
        SelectCourse.step1(message, ViewCourse.step2, None)

    @staticmethod
    def step2(message: telebot.types.Message,
              course_id: int):
        try:
            to_text = database_funcs.get_course_description(course_id)
            lessons = database_funcs.get_lessons_by_course(course_id)
            lessons.sort(key=lambda l: l.date)
            for num, l in enumerate(lessons):
                date = l.date.strftime('%m.%d.%Y %H:%M')
                to_text += f'\n\n{num + 1}: {l.name}\n{l.description}\nДата: {date}'
            bot.send_message(message.from_user.id, to_text,
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class ViewAccess:

    @bot.message_handler(commands=['view_access'])
    @staticmethod
    def step1(message: telebot.types.Message):
        user_id = database_funcs.get_user_id(str(message.from_user.id))
        lesson_ids = database_funcs.get_user_access_lessons(user_id)
        lessons = [database_funcs.get_lesson(lid) for lid in lesson_ids]
        lessons.sort(key=lambda l: l.date)
        to_text = 'Список доступных лекций:'
        for l in lessons:
            c_name = database_funcs.get_course_name(l.course_id)
            date = l.date.strftime('%m.%d.%Y %H:%M')
            to_text += f'\n\n{c_name}. {l.name}\n{l.description}\nДата: {date}'
        bot.send_message(message.from_user.id,
                         to_text,
                         reply_markup=BuildMarkup.menu(message.from_user.id))


class ToCartCourse:

    @bot.message_handler(commands=['to_cart_course'])
    @staticmethod
    def step1(message: telebot.types.Message):
        SelectCourse.step1(message, ToCartCourse.step2, None)

    def step2(message: telebot.types.Message,
              course_id: int):
        try:
            user_id = database_funcs.get_user_id(str(message.from_user.id))
            database_funcs.add_shopping_cart_course(user_id, course_id)
            bot.send_message(message.from_user.id,
                             'Курс добавлен в корзину',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class ToCartLesson:

    @bot.message_handler(commands=['to_cart_lesson'])
    @staticmethod
    def step1(message: telebot.types.Message):
        SelectLesson.step1(message, ToCartLesson.step2, None)

    def step2(message: telebot.types.Message,
              lesson_id: int):
        try:
            user_id = database_funcs.get_user_id(str(message.from_user.id))
            database_funcs.add_shopping_cart_lesson(user_id, lesson_id)
            bot.send_message(message.from_user.id,
                             'Лекция добавлена в корзину',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class CleanCart:

    @bot.message_handler(commands=['clean_cart'])
    @staticmethod
    def step1(message: telebot.types.Message):
        try:
            user_id = database_funcs.get_user_id(message.from_user.id)
            database_funcs.clean_shopping_cart(user_id)
            bot.send_message(message.from_user.id,
                             'Корзина очищена',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))


class Buy:

    @bot.message_handler(commands=['buy'])
    @staticmethod
    def buy(message: telebot.types.Message):
        user_id = database_funcs.get_user_id(message.from_user.id)
        payassigment = database_funcs.build_pay_assigment(user_id)
        if len(payassigment.lesson_ids) == 0:
            bot.send_message(message.from_user.id, 'Корзина пуста')
            return
        temp_payment_id = database_funcs.create_temp_payment(user_id,
                                                             payassigment)
        database_funcs.clean_shopping_cart(user_id)

        print(payassigment.prices)

        bot.send_invoice(
            chat_id=message.from_user.id,
            title='Курсы АГУ',
            description='Оплата курсов Адыгейского Государственного Унивреситете',
            invoice_payload=str(temp_payment_id),
            provider_token=config.SBERBANK_TOKEN,
            currency='RUB',
            prices=payassigment.prices
        )

    @bot.pre_checkout_query_handler(func=lambda query: True)
    @staticmethod
    def checkout(pre_checkout_query: telebot.types.PreCheckoutQuery):
        bot.answer_pre_checkout_query(pre_checkout_query.id,
                                      ok=True)

    @bot.message_handler(content_types=['successful_payment'])
    @staticmethod
    def got_payment(message: telebot.types.Message):
        database_funcs.on_success_payment(int(message.successful_payment.invoice_payload))
        bot.send_message(message.from_user.id,
                         'Вы были зачислены на оплаченные курсы. Ожидайте ссылку-приглашение',
                         reply_markup=BuildMarkup.menu(message.from_user.id))


class BotMain:

    @bot.message_handler(commands=['start'])
    @staticmethod
    def start(message: telebot.types.Message):
        database_funcs.add_user(str(message.from_user.id))
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id, 'Вы администратор!',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        else:
            bot.send_message(message.from_user.id, 'Добро пожаловать!',
                             reply_markup=BuildMarkup.menu(message.from_user.id))

    @bot.message_handler(content_types=['text'])
    @staticmethod
    def any_text(message: telebot.types.Message):

        if message.text == 'Обзор курсов':
            ViewCourses.step1(message)
        elif message.text == 'Обзор лекций':
            ViewCourse.step1(message)
        elif message.text == 'Приобрести лекцию':
            ToCartLesson.step1(message)
        elif message.text == 'Приобрести курс':
            ToCartCourse.step1(message)
        elif message.text == 'Доступные лекции':
            ViewAccess.step1(message)
        elif message.text == 'Оплатить':
            Buy.buy(message)
        elif message.text == 'Очистить корзину':
            CleanCart.step1(message)
        else:
            bot.send_message(message.from_user.id,
                            'Не распознано',
                            reply_markup=BuildMarkup.menu(message.from_user.id))


bot.polling()
