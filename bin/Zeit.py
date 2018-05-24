from .utils.Constant import *


class Zeit:
    Secret = 0

    def __init__(self, secret):
        self.Secret = secret

    def daily_zeit_menu(self, bot, update, user_data):
        self.dailyZeit(bot, update)

    def dailyZeit(self, bot, update):
        update.message.reply_text(not_yet_in_production)
