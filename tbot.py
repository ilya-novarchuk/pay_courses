

import telebot

import config
import database_funcs


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def is_admin(id: int | str) -> bool:
    if not isinstance(id, str):
        id = str(id)
    return id in config.TELEGRAM_ADMINS


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


@bot.message_handler(commands=['admin_view_cources'])
def admin_view_cources(message: telebot.types.Message):
    cources = database_funcs.get_cources()
    cources = [f'id: {c.id}\ndescription: {c.description}' for c in cources]
    to_text = '\n\n'.join(cources)
    bot.send_message(message.from_user.id, to_text)


#for admin in config.TELEGRAM_ADMINS:
#    bot.send_message(admin, 'Start')
bot.polling()

