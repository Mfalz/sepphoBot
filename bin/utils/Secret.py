from secrets import *


class Secret:
    authID = sepphobot_auth_id
    telegramToken = sepphobot_telegram_token

    def getTelegramToken(self):
        return self.telegramToken

    def getAuthID(self):
        return self.authID

    def isAuthorized(self, update):
        return update.message.from_user.id == self.getAuthID()
