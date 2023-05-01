

import telebot

import build_markup
import database_funcs
from bot_core import bot, is_admin


@bot.message_handler(commands=['create_course'])
def create_course(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id,
                         'Введите название курса:',
                         reply_markup=build_markup.space())
        bot.register_next_step_handler(message, create_course_step2)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')



@bot.message_handler(commands=['edit_course_name'])
def edit_course_name(message: telebot.types.Message):
    if is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, 'Выберите курс:',
                         reply_markup=build_markup.select_course())
        bot.register_next_step_handler(message, edit_course_name_step2)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор.')


def edit_course_name_step2(message: telebot.types.Message):
    try:
        course_name = message.text
        course_id = database_funcs.get_course_id(course_name)
        bot.send_message(message.from_user.id, 'Введите новое название:')
        bot.register_next_step_handler(message,
                                       edit_course_name_step3,
                                       course_id)
    except Exception as exp:
        bot.send_message(message.from_user.id, str(exp))


def edit_course_name_step3(message: telebot.types.Message,
                           course_id: int):
    new_name = message.text


def edit_course_description():
    pass

def edit_course_price():
    pass

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

