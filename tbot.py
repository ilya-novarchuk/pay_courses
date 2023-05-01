

import telebot

import config
import database_funcs


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def is_admin(id: int | str) -> bool:
    if not isinstance(id, str):
        id = str(id)
    return id in config.TELEGRAM_ADMINS


class BuildMarkup:

    def space() -> telebot.types.ReplyKeyboardMarkup:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    def menu(id) -> telebot.types.ReplyKeyboardMarkup:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns = []
        if is_admin(id):
            btns.append(telebot.types.KeyboardButton('/create_course'))
            btns.append(telebot.types.KeyboardButton('/edit_course_name'))
            btns.append(telebot.types.KeyboardButton('/edit_course_description'))
            btns.append(telebot.types.KeyboardButton('/edit_course_price'))
            btns.append(telebot.types.KeyboardButton('/delete_corse'))
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
    pass


class EditCourseDescription:
    pass


class EditCoursePrice:
    pass


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
