# import buttons as buttons
from telebot import types
import pickle
import os
import DZ
import fun

# -----------------------------------------------------------------------
class Users:
    activeUsers = {}

    def __init__(self, chat_id, user_json):
        self.id = user_json["id"]
        self.isBot = user_json["is_bot"]
        self.firstName = user_json["first_name"]
        self.userName = user_json["username"]
        self.languageCode = user_json.get("language_code", "")
        self.__class__.activeUsers[chat_id] = self

    def __str__(self):
        return f"Name user: {self.firstName}   id: {self.userName}   lang: {self.languageCode}"

    def getUserHTML(self):
        return f"Name user: {self.firstName}   id: <a href='https://t.me/{self.userName}'>{self.userName}</a>   lang: {self.languageCode}"

    @classmethod
    def getUser(cls, chat_id):
        return cls.activeUsers.get(chat_id)

# -----------------------------------------------------------------------
class KeyboardMenu:
    def __init__(self, name, handler=None):
        self.name = name
        self.handler = handler

# -----------------------------------------------------------------------
class Menu:
    hash = {}  # тут будем накапливать все созданные экземпляры класса
    cur_menu = {}  # тут будет находиться текущий экземпляр класса, текущее меню для каждого пользователя
    extendedParameters = {}  # это место хранения дополнительных параметров для передачи в inline кнопки
    namePickleFile = "bot_curMenu.plk"

    # ПЕРЕПИСАТЬ для хранения параметров привязанных к chat_id и названию кнопки
    def __init__(self, name, buttons=None, parent=None, module=""):
        self.parent = parent
        self.module = module
        self.name = name
        self.buttons = buttons
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        markup.add(*buttons)  # Обратите внимание - звёздочка используется для распаковки списка
        self.markup = markup
        self.__class__.hash[name] = self  # в классе содержится словарь, со всеми экземплярами класса, обновим его

    @classmethod
    def getExtPar(cls, id):
        return cls.extendedParameters.get(id, None)

    @classmethod
    def setExtPar(cls, parameter):
        import uuid
        id = uuid.uuid4().hex
        cls.extendedParameters[id] = parameter
        return id

    @classmethod
    def getMenu(cls, chat_id, name):
        menu = cls.hash.get(name)
        if menu != None:
            cls.cur_menu[chat_id] = menu
            cls.saveCurMenu()
        return menu

    @classmethod
    def getCurMenu(cls, chat_id):
        return cls.cur_menu.get(chat_id)

    @classmethod
    def loadCurMenu(self):
        if os.path.exists(self.namePickleFile):
            with open(self.namePickleFile, 'rb') as pickle_in:
                self.cur_menu = pickle.load(pickle_in)
        else:
            self.cur_menu = {}

    @classmethod
    def saveCurMenu(self):
        with open(self.namePickleFile, 'wb') as pickle_out:
            pickle.dump(self.cur_menu, pickle_out)


# -----------------------------------------------------------------------
def goto_menu(bot, chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        return target_menu
    else:
        return None


# -----------------------------------------------------------------------
m_main = Menu("Главное меню", buttons=["Развлечения", "Игры", "ДЗ", "Помощь"])
m_games = Menu("Игры", buttons=["Игра \"Быстрый счет\"-MP", "Выход"], module="botGames", parent=m_main)
m_game_21 = Menu("Игра в 21", buttons=["Карту!", "Стоп!", "Выход"], parent=m_games, module="botGames")
m_game_rsp = Menu("Игра КНБ", buttons=["☝🏻", "✌🏼", "🤟🏻", "🖖🏻", "🖐🏻", "Выход"], parent=m_games, module="botGames")
m_DZ = Menu("ДЗ", buttons=["Задание-1", "Задание-2", "Задание-3", "Задание-4", "Задание-5", "Задание-6","Задание-7","Задание-8", "Задание-9", "Выход"], parent=m_main, module="DZ")
m_fun = Menu("Развлечения", buttons=["Прислать собаку", "Прислать лису", "Прислать анекдот",  "Прислать новости", "Прислать фильм", "Угадай кто?", "Прислать гороскоп",'Прислать кота', "Выход"], parent=m_main, module="fun")
m_voice = Menu("Голос!", buttons=["Текущее время", "Произнеси текст", "Главные новости", "Прогноз погоды", "Выход"], parent=m_main, module="speech")
# m_fun = Menu("Развлечения", buttons=[["Прислать собаку", "Прислать лису"], ["Прислать анекдот", "Прислать фильм"], ["Выход"]], parent=m_main)

Menu.loadCurMenu()

# import main
# import DZ
#
# b_exit = KeyboardMenu("Выход")
#
# b_fun = KeyboardMenu("Развлечения")
# b_game = KeyboardMenu("Игры")
# b_dz = KeyboardMenu("ДЗ")
# b_help = KeyboardMenu("Помощь", main.send_help)
# m_main = Menu("Главное меню", buttons=[b_fun, b_game, b_dz, b_help])
#
# b_dz1 = KeyboardMenu("Задание-1", DZ.dz1)
# b_dz2 = KeyboardMenu("Задание-2", DZ.dz2)
# b_dz3 = KeyboardMenu("Задание-3", DZ.dz3)
# b_dz4 = KeyboardMenu("Задание-4", DZ.dz4)
# b_dz5 = KeyboardMenu("Задание-5", DZ.dz5)
# b_dz6 = KeyboardMenu("Задание-6", DZ.dz6)
#
# m_DZ = Menu(b_dz, buttons=[b_dz1, b_dz2, b_dz3, b_dz4, b_dz5, b_dz6, b_exit], parent=m_main)
#
# menu_json = {
#     "name": "Главное меню",
#     "handler": "",
#     "buttons": [
#         {
#             "name": "Развлечения",
#             "handler": "",
#         },
#         {
#             "name": "Игры",
#             "handler": "",
#         },
#         {
#             "name": "ДЗ",
#             "handler": "",
#         },
#         {
#             "name": "Помощь",
#             "handler": "main.send_help",
#         }
#     ]
# }


