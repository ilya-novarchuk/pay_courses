

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

    def menu(id) -> telebot.types.ReplyKeyboardMarkup:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns = []
        if is_admin(id):
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
        btns.append('Обзор курсов')
        btns.append('Обзор лекций')
        markup.add(*btns)
        return markup

    def select_course() -> telebot.types.ReplyKeyboardMarkup:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        courses = database_funcs.get_courses()
        btns = [telebot.types.KeyboardButton(c.name) for c in courses]
        markup.add(*btns)
        return markup

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


class EditCourseName:

    @bot.message_handler(commands=['edit_course_name'])
    @staticmethod
    def step1(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id,
                             'Выберите курс:',
                             reply_markup=BuildMarkup.select_course())
            bot.register_next_step_handler(message, EditCourseName.step2)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            bot.send_message(message.from_user.id,
                             'Введите новое название:')
            bot.register_next_step_handler(message, EditCourseName.step3, course_id)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

    @staticmethod
    def step3(message: telebot.types.Message,
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
            bot.send_message(message.from_user.id,
                             'Выберите курс:',
                             reply_markup=BuildMarkup.select_course())
            bot.register_next_step_handler(message, EditCourseDescription.step2)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            bot.send_message(message.from_user.id,
                             'Введите новое описание:')
            bot.register_next_step_handler(message, EditCourseDescription.step3, course_id)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

    @staticmethod
    def step3(message: telebot.types.Message,
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
            bot.send_message(message.from_user.id,
                             'Выберите курс:',
                             reply_markup=BuildMarkup.select_course())
            bot.register_next_step_handler(message, EditCoursePrice.step2)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            bot.send_message(message.from_user.id,
                             'Введите новую цену:')
            bot.register_next_step_handler(message, EditCoursePrice.step3, course_id)
        except Exception as exp:
            bot.send_message(message.from_user.id, str(exp))

    @staticmethod
    def step3(message: telebot.types.Message,
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
            bot.send_message(message.from_user.id,
                             'Выберите курс:',
                             reply_markup=BuildMarkup.select_course())
            bot.register_next_step_handler(message, DeleteCourse.step2)
        else:
            bot.send_message(message.from_user.id, 'Вы не администратор.')

    @staticmethod
    def step2(message: telebot.types.Message):
        try:
            course_name = message.text
            course_id = database_funcs.get_course_id(course_name)
            database_funcs.delete_course(course_id)
            bot.send_message(message.from_user.id, 'Курс удален.',
                             reply_markup=BuildMarkup.menu())
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

    def step1(message: telebot.types.Message,
              callback_func: Callable[[telebot.types.Message, int | None], None],
              post_message: str):
        bot.send_message(message.from_user.id,
                         'Выберите курс:',
                         reply_markup=BuildMarkup.select_course())
        bot.register_next_step_handler(message, SelectLesson.step2,
                                       callback_func, post_message)

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

    def step3(message: telebot.types.Message,
              course_id: int,
              callback_fund: Callable[[telebot.types.Message, int | None], None],
              post_message: str):
        try:
            lesson_name = message.text
            lesson_id = database_funcs.get_lesson_id(course_id, lesson_name)
            if post_message is not None:
                bot.send_message(message.from_user.id, post_message)
                bot.register_next_step_handler(message,
                                               callback_fund,
                                               lesson_id)
            else:
                callback_fund(message, lesson_id)
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


class BotMain:

    @bot.message_handler(commands=['start'])
    def start(message: telebot.types.Message):
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id, 'Вы администратор!',
                             reply_markup=BuildMarkup.menu(message.from_user.id))
        else:
            bot.send_message(message.from_user.id, 'Добро пожаловать!',
                             reply_markup=BuildMarkup.menu(message.from_user.id))

    @bot.message_handler(content_types=['text'])
    def any_text(message: telebot.types.Message):
        bot.send_message(message.from_user.id,
                         'Не распознано',
                         reply_markup=BuildMarkup.menu(message.from_user.id))


bot.polling()
