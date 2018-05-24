from .utils.Constant import *


class Nas:
    Secret = 0

    def __init__(self, secret):
        self.Secret = secret

    def get_photo_menu(self, bot, update, user_data):
        self.getPhoto(bot, update)

    def getPhoto(self, bot, update):
        update.message.reply_text(not_yet_in_production)
