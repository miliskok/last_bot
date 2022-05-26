import telebot
from telebot import types
from random import *


gameb = ['Камень', 'Ножницы', 'Бумага']


def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)
# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler

def dz1(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    myname = 'Арина'
    bot.send_message(chat_id, text="Привет, меня зовут " + myname)
def dz2(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    myname = 'Арина'
    myage = '18'
    bot.send_message(chat_id, text="Привет, меня зовут " + myname + ', мне ' + myage)
def dz3(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    myname = 'Арина'
    myname2 = myname * 5
    bot.send_message(chat_id, text="Мое имя 5 раз подряд: " + myname2)

def dz4(bot, chat_id, message):
    bot.send_message(chat_id, 'Как тебя зовут?')
    bot.register_next_step_handler(message, dz4_1, bot)

def dz4_1( message, bot):
    bot.send_message(message.chat.id, f'Приятно познакомиться, {message.text} \nСколько тебе лет?')
    bot.register_next_step_handler(message, dz4_2, bot)

def dz4_2(message, bot):
    if message.text.isnumeric()== True:
        bot.send_message(message.chat.id, f'Тебе уже {message.text}! Впринципе, выглядишь вполне на свой возраст)')
    while message.text.isnumeric() == False:
        bot.send_message(message.chat.id, 'Введите верный возраст!!')
        break



def dz5(bot, chat_id, message):
    bot.send_message(chat_id, "Как тебя зовут?")
    bot.register_next_step_handler(message, dz5_1, bot)

def dz5_1(message, bot):
    global name2
    name2 = message.text
    name2 = name2[7::-1]
    bot.send_message(message.chat.id, "Наоборот вот так" + ' ' + name2)

def dz6(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id,
                                                           f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)

def dz7(bot, chat_id, message):
    bot.send_message(chat_id, 'Как тебя зовут?')
    bot.register_next_step_handler(message, dz7_1, bot)

def dz7_1(message, bot):
    global name4
    name4 = message.text
    if name4.islower() == True:
        bot.send_message(message.chat.id, 'Есть нижний регитср')
    elif name4.isupper() == True:
        bot.send_message(message.chat.id, 'Есть верхний регитср')
    else:
        bot.send_message(message.chat.id, 'Есть верхний регитср и нижний')

def dz8(bot, chat_id, message):
    bot.send_message(chat_id, "Как тебя зовут?")
    bot.register_next_step_handler(message, dz8_1, bot)

def dz8_1(message, bot):
    global name5
    name5 = message.text
    for i in name5:
        if i == " ":
            bot.send_message(message.chat.id, 'Введите имя без пробелов')

        elif i == "0" or i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9":
            bot.send_message(message.chat.id, 'Введите имя без цифр')

    bot.send_message(message.chat.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, dz8_2, bot)
def dz8_2(message, bot):
    global age5
    age5 = int(message.text)
    while age5 == 0:
        try:
            age5 = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, "Вводите коректные цифры!!!!")
    if age5 < 150 and age5 > 0:
        bot.send_message(message.chat.id,
                         ' Твоё имя без ошибок ' + name5 + ' Нормальный возраст ' + ' ' + str(age5) + ' ')

def dz9(bot, chat_id, message):
    bot.send_message(chat_id, '2+2*2?')
    bot.register_next_step_handler(message, dz9_1, bot)

def dz9_1(message, bot):
    global age
    age = int(message.text)
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, "Вводите цифры!!!!")
    if age == 6:
        bot.send_message(message.chat.id, "Правильно")
    else:
        bot.send_message(message.chat.id, "Попробуй еще раз")
    age = 0


# -----------------------------------------------------------------------


def dz10(bot, chat_id, message):
    bot.send_message(chat_id, 'Камень, ножницы или бумага?')
    bot.register_next_step_handler(message, reg_game, bot)
def reg_game(message, bot):
    global game
    global gameb
    global value
    value = choice(gameb)
    game = message.text
    if game == 'Камень' or game == 'камень':
        if value == 'Камень' or value == 'камень':
            bot.send_message(message.chat.id, 'Ничья)))')
        if value == 'Ножницы' or value == 'ножницы':
            bot.send_message(message.chat.id, 'Вы победили, я поставила ножницы')
        if value == 'Бумага' or value == 'бумага':
            bot.send_message(message.chat.id, 'Вы проиграли , я поставила бумагу')
    if game == 'Ножницы' or game == 'ножницы':
        if value == 'Камень' or value == 'камень':
            bot.send_message(message.chat.id, 'Вы проиграли , я поставила камень')
        if value == 'Ножницы' or value == 'ножницы':
            bot.send_message(message.chat.id, 'Ничья))')
        if value == 'Бумага' or value == 'бумага':
            bot.send_message(message.chat.id, 'Вы выиграли , я поставила бумагу')
    if game == 'Бумага' or game == 'бумага':
        if value == 'Камень' or value == 'камень':
            bot.send_message(message.chat.id, 'Вы выиграли , я поставила камень')
        if value == 'Ножницы' or value == 'ножницы':
            bot.send_message(message.chat.id, 'Вы проиграли , я поставила ножницы')
        if value == 'Бумага' or value == 'бумага':
            bot.send_message(message.chat.id, 'Ничья)))')
