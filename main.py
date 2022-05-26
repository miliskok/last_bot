# Телеграм-бот v.002 - бот создаёт меню, присылает собачку, и анекдот

import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types
import DZ
import requests
bot = telebot.TeleBot('5106619300:AAFyqqh_FvARsb5E_sATTgar1De4cqgjHOE')  # Создаем экземпляр бота

# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
def inputBot(message, text):
    a = []
    def ret(message):
        a.clear()
        a.append(message.text)
        return False

    a.clear()
    mes = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ret)
    while a == []:
        pass
    return a[0]
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Главное меню")
    btn2 = types.KeyboardButton("❓ Помощь")
    markup.add(btn1, btn2)

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке ПаЙтон".format(
                         message.from_user), reply_markup=markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Главное меню" or ms_text == "👋 Главное меню" or ms_text == "Вернуться в главное меню":  # ..........
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Развлечения")
        btn2 = types.KeyboardButton("WEB-камера")
        btn3 = types.KeyboardButton("Управление")
        btn4 = types.KeyboardButton('дз')
        back = types.KeyboardButton("Помощь")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(chat_id, text="Вы в главном меню", reply_markup=markup)

    elif ms_text == "Развлечения":  # ..................................................................................
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Прислать собаку")
        btn2 = types.KeyboardButton("Прислать анекдот")
        btn3 = types.KeyboardButton("Прислать гороскоп")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(chat_id, text="Развлечения", reply_markup=markup)

    elif ms_text == 'Прислать гороскоп':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        req_goro = requests.get('https://horo.mail.ru')
        soup = bs4.BeautifulSoup(req_goro.text, 'html.parser')
        result_find = soup.findAll('div', class_="article__item article__item_alignment_left article__item_html")
        bot.send_message(chat_id, text=str(result_find))

    elif ms_text == "/dog" or ms_text == "Прислать собаку":  # .........................................................
        bot.send_message(chat_id, text="🐕")

    elif ms_text == "Прислать анекдот":  # .............................................................................
        bot.send_message(chat_id, text= "Мне можно доверять свои секреты, хотя бы потому что, я на следующий день их забуду.")

    elif ms_text == "WEB-камера":
        img2 = open('кот.jpg', 'rb')
        bot.send_photo(message.chat.id, img2)

    elif ms_text == "Управление":  # ...................................................................................
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "Помощь" or ms_text == "/help":  # .................................................................
        bot.send_message(chat_id, "Автор: Мясникова Милана")
        key1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Напишите мне", url="https://t.me/p1zdyushka")
        key1.add(btn1)
        img3 = open('пип.png', 'rb')
        bot.send_photo(chat_id, img3, reply_markup=key1)

    elif ms_text == 'дз':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        p1 = types.KeyboardButton('Задание 1')
        p2 = types.KeyboardButton('Задание 2')
        p3 = types.KeyboardButton('Задание 3')
        p4 = types.KeyboardButton('Задание 4')
        p5 = types.KeyboardButton('Задание 5')
        p6 = types.KeyboardButton('Задание 6')
        p7 = types.KeyboardButton('Задание 7')
        p8 = types.KeyboardButton('Задание 8')
        p9 = types.KeyboardButton('Задание 9')
        p10 = types.KeyboardButton('Задание 10')
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, back)
        bot.send_message(chat_id, text='дз', reply_markup=markup)
    elif ms_text == 'Задание 1':
        DZ.dz1(bot, chat_id)
    elif ms_text == 'Задание 2':
        DZ.dz2(bot, chat_id)
    elif ms_text == 'Задание 3':
        DZ.dz3(bot, chat_id)
    elif ms_text == 'Задание 4':
        DZ.dz4(bot, chat_id, message)
    elif ms_text == 'Задание 5':
        DZ.dz5(bot, chat_id, message)
    elif ms_text == "Задание 6":
        DZ.dz6(bot, chat_id)
    elif ms_text == "Задание 7":
        DZ.dz7(bot, chat_id, message)
    elif ms_text == "Задание 8":
        DZ.dz8(bot, chat_id, message)
    elif ms_text == "Задание 9":
        DZ.dz9(bot, chat_id, message)
    elif ms_text == "Задание 10":
        DZ.dz10(bot, chat_id, message)



    else:# ...........................................................................................................
        bot.send_message(chat_id, text="Я тебя слышу!!! Ваше сообщение: " + ms_text)

# -----------------------------------------------------------------------
bot.polling(none_stop=True, interval=0) # Запускаем бота

print()