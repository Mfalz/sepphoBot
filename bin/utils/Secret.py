class Secret:
    authID = ""
    telegramToken = ""
    userID = 0

    def __init__(self, userID, telegramToken):
        self.telegramToken=telegramToken
        self.authID=userID

    def isAuthorized(self):
        return self.userID == self.authID

    def getTelegramToken(self):
        return self.telegramToken

    def getAuthID(self):
        return self.authID

    def setUser(self, bot, update):
        self.userID = update.message.from_user.id