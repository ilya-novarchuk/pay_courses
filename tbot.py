

import dateparser
import telebot

import config
import database_funcs


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def is_admin(id: int | str) -> bool:
    if not isinstance(id, str):
        id = str(id)
    return id in config.TELEGRAM_ADMINS


# # #
# # # COURSE MANAGMENT
# # #


@bot.message_handler(commands=['create_course'])
def create_course(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Введите описание курса:')
        bot.register_next_step_handler(message, write_course_description)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def write_course_description(message: telebot.types.Message):
    description = message.text
    database_funcs.create_course(description)
    bot.send_message(message.from_user.id, 'Курс создан.')


@bot.message_handler(commands=['edit_course'])
def edit_course(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Введите id курса:')
        bot.register_next_step_handler(message, edit_course_read_id)    
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def edit_course_read_id(message: telebot.types.Message):
    bot.send_message(message.from_user.id, 'Введите новое описание:')
    id = int(message.text)
    bot.register_next_step_handler(message, edit_course_read_description, id)


def edit_course_read_description(message: telebot.types.Message, id: int):
    description = message.text
    try:
        database_funcs.edit_course(id, description)
        bot.send_message(message.from_user.id, 'Описание курса обновлено.')
    except Exception as exp:
        bot.send_message(message.from_user.id, str(exp))


@bot.message_handler(commands=['delete_course'])
def delete_course(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Введите id курса:')
        bot.register_next_step_handler(message, delete_course_read_id)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def delete_course_read_id(message: telebot.types.Message):
    id = int(message.text)
    database_funcs.delete_course(id)
    bot.send_message(message.from_user.id, 'Курс со всеми лекциями удален')

# # #
# # # COURSE MANAGMENT END
# # #


# # #
# # # LESSON MANAGMENT
# # #


@bot.message_handler(commands=['create_lesson'])
def create_lesson(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Введите id курса:')
        bot.register_next_step_handler(message, create_lesson_read_id)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def create_lesson_read_id(message: telebot.types.Message):
    try:
        id = int(message.text)
        if database_funcs.course_exist(id):
            bot.send_message(message.from_user.id, 'Введите описание:')
            bot.register_next_step_handler(message, create_lesson_read_description, id)
        else:
            bot.send_message(message.from_user.id, 'Курс не существует.')
    except Exception as exp:
        bot.send_message(message.from_user.id, str(exp))


def create_lesson_read_description(message: telebot.types.Message, id: int):
    description = message.text
    bot.send_message(message.from_user.id, 'Введите дату:')
    bot.register_next_step_handler(message, create_lesson_read_date, id, description)


def create_lesson_read_date(message: telebot.types.Message,
                            id: int,
                            description: str):
    try:
        date = dateparser.parse(message.text)
        database_funcs.create_lesson(id, description, date)
        bot.send_message(message.from_user.id, 'Лекция создана.')
    except Exception as exp:
        bot.send_message(message.from_user.id, str(exp))


@bot.message_handler(commands=['edit_lesson'])
def edit_lesson(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Введите id курса:')
        bot.register_next_step_handler(message, edit_lesson_read_id)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def edit_lesson_read_id(message: telebot.types.Message):
    id = int(message.text)
    if database_funcs.lesson_exist(id):
        bot.send_message(message.from_user.id, 'Введите новое описание:')
        bot.register_next_step_handler(message, edit_lesson_read_description, id)
    else:
        bot.send_message(message.from_user.id, 'Лекция не существует.')


def edit_lesson_read_description(message: telebot.types.Message,
                                 id: int):
    description = message.text
    bot.send_message(message.from_user.id, 'Введите новую дату:')
    bot.register_next_step_handler(message, edit_lesson_read_date, id, description)


def edit_lesson_read_date(message: telebot.types.Message,
                          id: int,
                          description: str):
    date = dateparser.parse(message.text)
    try:
        database_funcs.edit_lesson(id, description, date)
        bot.send_message(message.from_user.id, 'Лекция обновлена.')
    except Exception as exp:
        bot.send_message(message.from_user.id, str(exp))


@bot.message_handler(commands=['delete_lesson'])
def delete_lesson(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Введите id лекции:')
        bot.register_next_step_handler(message, delete_lesson_read_id)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def delete_lesson_read_id(message: telebot.types.Message):
    id = int(message.text)
    if database_funcs.lesson_exist(id):
        database_funcs.delete_lesson(id)
        bot.send_message(message.from_user.id, 'Лекция удалена.')
    else:
        bot.send_message(message.from_user.id, 'Лекция не существует.')


# # #
# # # LESSON MANAGMENT END
# # #


@bot.message_handler(commands=['admin_view_courses'])
def admin_view_courses(message: telebot.types.Message):
    courses = database_funcs.get_courses()
    courses = [f'id: {c.id}\ndescription: {c.description}' for c in courses]
    to_text = '\n\n'.join(courses)
    bot.send_message(message.from_user.id, to_text)


@bot.message_handler(commands=['admin_view_lessons'])
def admin_view_lessons(message: telebot.types.Message):
    lessons = database_funcs.get_lessons()
    lessons = [
        f'id: {l.id}\ncourse: {l.course_id}\ndescription: {l.description}\ndate: {l.date}'
        for l in lessons
    ]
    to_text = '\n\n'.join(lessons)
    bot.send_message(message.from_user.id, to_text)


#for admin in config.TELEGRAM_ADMINS:
#    bot.send_message(admin, 'Start')
bot.polling()

