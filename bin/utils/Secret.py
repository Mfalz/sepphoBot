class Secret:
    authID = "yourID"
    telegramToken = "telegramToken"

    def getTelegramToken(self):
        return self.telegramToken

    def getAuthID(self):
        return self.authID

    def isAuthorized(self, update):
        return update.message.from_user.id == self.Secret.getAuthID()