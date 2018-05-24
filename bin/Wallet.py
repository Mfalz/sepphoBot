from .utils.Constant import *


class Wallet:
    Secret = 0

    def __init__(self, secret):
        self.Secret = secret

    def wallet_menu(self, bot, update, user_data):
        self.wallet(bot, update)

    def wallet(self, bot, update):
        update.message.reply_text(not_yet_in_production)
