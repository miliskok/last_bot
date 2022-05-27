import requests
import threading
from telebot import types
from menuBot import Menu, goto_menu

# -----------------------------------------------------------------------
# вместо того, что бы делать еще один класс, обойдёмся без него - подумайте, почему и как
activeGames = {}  # Тут будем накапливать все активные игры. У пользователя может быть только одна активная игра


def newGame(chatID, newGame):
    activeGames.update({chatID: newGame})
    return newGame


def getGame(chatID):
    return activeGames.get(chatID, None)


def stopGame(chatID):
    activeGames.pop(chatID, None)


# def looper(classGame):
#     if classGame.gameTimeLeft > 0:
#         classGame.gameTimeLeft -= 1
#         # print(classGame.gameTimeLeft)
#         classGame.setTextGame()
#         threading.Timer(1, looper, args=[classGame]).start()
#
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
class GameRPS_Multiplayer:
    game_duration = 10  # сек.
    values = ["☝🏻", "✌🏼", "🤟🏻", "🖖🏻", "🖐🏻"]
    real_values = [1, 2, 2, 3, 5]
    result = 0
    message_to_delete = []
    name = "Игра \"Быстрый счет\" (Мультиплеер)"
    text_rules = "<b>Победитель определяется по следующим правилам:</b>\n" \
                 "Начинается эта игра так же, как «Камень, ножницы, бумага». " \
                 "Игроки сжимают руки в кулаки, качают им, считают вслух, " \
                 "а потом одновременно разжимают кулаки. Только в этой версии " \
                 "вместо знаков нужно пальцами показывать какое-то число. " \
                 "Заранее договоритесь, будут игроки показывать числа на обеих " \
                 "руках или на одной. Затем игрокам нужно быстро сложить числа, " \
                 "показанные ими, и выкрикнуть ответ. Побеждает тот, " \
                 "кто выкрикнет первым. Да, это небольшой урок математики, " \
                 "замаскированный под обычную игру. С ее помощью можно отработать и " \
                 "остальные математические действия"
    # url_picRules = "https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg"

    class Player:

        def __init__(self, playerID, playerName):
            self.id = playerID
            self.gameMessage = None
            self.name = playerName
            self.scores = 0
            self.choice = 0
            self.lastChoice = ""

        def __str__(self):
            return self.name

    def __init__(self, bot, chat_user):
        self.id = chat_user.id
        self.gameNumber = 1  # счётчик сыгранных игр
        self.objBot = bot
        self.players = {}
        self.gameTimeLeft = 0
        self.objTimer = None
        self.winner = None
        self.lastWinner = None
        self.textGame = ""
        # self.addPlayer(None, "Компьютер")
        self.addPlayer(chat_user.id, chat_user.userName)

    def addPlayer(self, playerID, playerName):
        newPlayer = self.Player(playerID, playerName)
        self.players[playerID] = newPlayer
        self.startTimer()  # при присоединении нового игрока перезапустим таймер
        self.setTextGame()
        # создадим в чате пользователя игровое сообщение с кнопками, и сохраним его для последующего редактирования
        # url_picRules = self.url_picRules
        keyboard = types.InlineKeyboardMarkup()
        list_btn = []
        for i in range(len(self.values)):
            keyName = self.values[i]
            keyValue = self.real_values[i]
            list_btn.append(types.InlineKeyboardButton(text=keyName, callback_data=f"GameRPSm|Choice-{keyValue}|{Menu.setExtPar(self)}"))
        keyboard.add(*list_btn)
        list_btn = types.InlineKeyboardButton(text="Выход", callback_data="GameRPSm|Exit|" + Menu.setExtPar(self))
        keyboard.add(list_btn)
        gameMessage = self.objBot.send_message(playerID, text=self.textGame, parse_mode='HTML', reply_markup=keyboard)
        self.players[playerID].gameMessage = gameMessage
        self.sendMessagesAllPlayers([playerID])  # отправим всем остальным игрокам информацию о новом игроке
        return newPlayer

    def delPlayer(self, playerID):
        print("DEL")
        remotePlayer = self.players.pop(playerID)
        try:
            self.objBot.delete_message(chat_id=remotePlayer.id, message_id=remotePlayer.gameMessage.id)
        except:
            pass
        self.objBot.send_message(chat_id=remotePlayer.id, text="Мне жаль, вас выкинуло из игры!")
        goto_menu(self.objBot, remotePlayer.id, "Игры")
        self.startSecondStage()  # как только игрок выходит, проверим среди оставшихся есть ли победитель
        if len(self.players.values()) == 0:
            stopGame(self.id)

    def getPlayer(self, chat_userID):
        return self.players.get(chat_userID)

    def newGame(self):
        self.gameNumber += 1
        self.lastWinner = self.winner
        self.winner = None
        for player in self.players.values():
            player.lastChoice = player.choice
            player.choice = None
        self.startTimer()  # запустим таймер игры (если таймер активен, сбросим его)

    def looper(self):
        print("LOOP", self.objTimer)
        if self.gameTimeLeft > 0:
            self.setTextGame()
            self.sendMessagesAllPlayers()
            self.gameTimeLeft -= 1
            self.objTimer = threading.Timer(1, self.looper)
            self.objTimer.start()
            print(self.objTimer.name, self.gameTimeLeft)
        else:
            delList = []
            for player in self.players.values():
                if player.choice is None:
                    delList.append(player.id)
            for idPlayer in delList:
                self.delPlayer(idPlayer)

    def startTimer(self):
        print("START")
        self.stopTimer()
        self.gameTimeLeft = self.game_duration
        self.looper()

    def stopTimer(self):
        print("STOP")
        self.gameTimeLeft = 0
        if self.objTimer is not None:
            self.objTimer.cancel()
            self.objTimer = None

    def checkEndGame(self):
        isEndGame = True
        for player in self.players.values():
            isEndGame = isEndGame and player.choice != None
        return isEndGame

    def playerChoice(self, chat_userID, сhoice):
        player = self.getPlayer(chat_userID)
        player.choice = сhoice
        self.result += int(player.choice)
        self.startSecondStage()
        self.sendMessagesAllPlayers()

    def startSecondStage(self):
        if self.checkEndGame():
            self.stopTimer()
            for player in self.players.values():
                player.lastChoice = player.choice
                message = self.objBot.send_message(chat_id=player.id, text="Введите число.\n")
                self.message_to_delete.append(message)
        self.setTextGame()

        # if self.checkEndGame():
        #     self.stopTimer()  # все успели сделать ход, таймер выключаем
        #
        #     playersChoice = []
        #     for player in self.players.values():
        #         playersChoice.append(player.choice)
        #     choices = dict(zip(playersChoice, [playersChoice.count(i) for i in playersChoice]))
        #     if len(choices) == 1 or len(choices) == len(self.__class__.values):
        #         # если все выбрали одно значение, или если присутствуют все возможные варианты - это ничья
        #         self.winner = "Ничья"
        #     else:
        #         # к этому моменту останется всего два варианта, надо понять есть ли уникальный он и бьёт ли он других
        #         choice1, quantity1 = choices.popitem()
        #         choice2, quantity2 = choices.popitem()
#
        #         code = choice1[0] + choice2[0]
        #         if quantity1 == 1 and code == "КН" or code == "БК" or code == "НБ":
        #             choiceWiner = choice1
        #         elif quantity2 == 1 and code == "НК" or code == "КБ" or code == "БН":
        #             choiceWiner = choice2
        #         else:
        #             choiceWiner = None
#
        #         if choiceWiner != None:
        #             winner = ""
        #             for player in self.players.values():
        #                 if player.choice == choiceWiner:
        #                     winner = player
        #                     winner.scores += 1
        #                     break
        #             self.winner = winner
#
        #         else:
        #             self.winner = "Ничья"
        # self.setTextGame()
#
        # if self.checkEndGame() and len(self.players) > 1:  # начинаем новую партию через 3 секунды
        #     self.objTimer = threading.Timer(3, self.newGame)
        #     self.objTimer.start()

    def endGame(self):
        self.winner.scores += 1
        self.setTextGame()
        self.sendMessagesAllPlayers()
        stopGame(self.id)
        for message in self.message_to_delete:
            self.objBot.delete_message(chat_id=message.chat.id, message_id=message.id)

    def setTextGame(self):
        from prettytable import PrettyTable
        mytable = PrettyTable()
        mytable.field_names = ["Игрок", "Счёт", "Выбор", "Результат"]  # имена полей таблицы
        for player in self.players.values():
            mytable.add_row([player.name, player.scores, player.lastChoice, "Победитель!" if self.lastWinner == player else ""])

        textGame = self.text_rules + "\n\n"
        textGame += "<code>" + mytable.get_string() + "</code>" + "\n\n"

        if self.winner is None:
            textGame += f"Идёт игра... <b>Осталось времени для выбора: {self.gameTimeLeft}</b>\n"
        elif self.winner == "Ничья":
            textGame += f"<b>Ничья!</b> Пауза 3 секунды..."
        else:
            textGame += f"Выиграл: <b>{self.winner}!</b>"

        self.textGame = textGame

    def sendMessagesAllPlayers(self, excludingPlayers=()):
        try:
            for player in self.players.values():
                if player.id not in excludingPlayers:
                    textIndividual = f"\n Ваш выбор: {player.choice}, ждём остальных!" if player.choice is not None else "\n"
                    self.objBot.edit_message_text(chat_id=player.id, message_id=player.gameMessage.id, text=self.textGame + textIndividual, parse_mode='HTML',
                                                     reply_markup=player.gameMessage.reply_markup)
        except:
            pass

# -----------------------------------------------------------------------
def callback_worker(bot, cur_user, cmd, par, call):
    chat_id = call.message.chat.id
    message_id = call.message.id

    if cmd == "newGame":
        # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
        bot.delete_message(chat_id, message_id)
        newGame(chat_id, GameRPS_Multiplayer(bot, cur_user))
        bot.answer_callback_query(call.id)

    elif cmd == "Join":
        # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
        bot.delete_message(chat_id, message_id)
        gameRSPMult = Menu.getExtPar(par)
        if gameRSPMult is None:  # если наткнулись на кнопку, которой быть не должно
            return
        else:
            gameRSPMult.addPlayer(cur_user.id, cur_user.userName)
        bot.answer_callback_query(call.id)

    elif cmd == "Exit":
        bot.delete_message(chat_id, message_id)
        gameRSPMult = Menu.getExtPar(par)
        if gameRSPMult is not None:
            gameRSPMult.delPlayer(cur_user.id)
        goto_menu(bot, chat_id, "Игры")
        bot.answer_callback_query(call.id)

    elif "Choice-" in cmd:
        gameRSPMult = Menu.getExtPar(par)
        if gameRSPMult is None:  # если наткнулись на кнопку, которой быть не должно - удалим её из чата
            bot.delete_message(chat_id, message_id)
        else:
            choice = cmd[7:]
            gameRSPMult.playerChoice(cur_user.id, choice)
        bot.answer_callback_query(call.id)


# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    # ======================================= реализация игры БС Multiplayer
    if ms_text == "Игра \"Быстрый счет\"-MP":
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Создать новую игру", callback_data="GameRPSm|newGame")
        keyboard.add(btn)
        numGame = 0
        for game in activeGames.values():
            numGame += 1
            btn = types.InlineKeyboardButton(text="Игра БС-" + str(numGame) + " игроков: " + str(len(game.players)), callback_data="GameRPSm|Join|" + Menu.setExtPar(game))
            keyboard.add(btn)
        btn = types.InlineKeyboardButton(text="Вернуться", callback_data="GameRPSm|Exit")
        keyboard.add(btn)

        bot.send_message(chat_id, text=GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(chat_id, "Вы хотите начать новую игру, или присоединиться к существующей?", reply_markup=keyboard)



# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("Этот код должен использоваться ТОЛЬКО в качестве модуля!")