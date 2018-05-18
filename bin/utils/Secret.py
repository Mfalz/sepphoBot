class Secret:
    authID = ""
    telegramToken = ""
    userID = 0

    def __init__(self, userID, telegramToken):
        self.telegramToken=telegramToken
        self.authID=userID

    def isAuthorized(self):
        return false
        id_user = update.message.from_user.id
        if (int(id_user) != int(sepphobot_auth_id)):
            return False
        return True

    def getTelegramToken(self):
        return self.telegramToken

    def getAuthID(self):
        return self.authID

    def setUser(self, bot, update):
        self.userID = update.message.from_user.id