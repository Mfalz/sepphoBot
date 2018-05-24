from .utils.Constant import *


class Deal:
    Secret = 0

    def __init__(self, secret):
        self.Secret = secret

    def getCostMin(self, bot, update):
        update.message.reply_text(not_yet_in_production)

    def day_deal_menu(self, bot, update, user_data):
        self.dayDeal(bot, update)

    def dayDeal(self, bot, update):
        update.message.reply_markdown("[Look for the daily deal!](https://www.daydeal.ch/).")

    def week_deal_menu(self, bot, update, user_data):
        self.weekDeal(bot, update)

    def weekDeal(self, bot, update):
        update.message.reply_markdown("[Look for the weekly deal!](https://www.daydeal.ch/deal-of-the-week).")

    def digitec_deal_menu(self, bot, update, user_data):
        self.digitecDeal(bot, update)

    def digitecDeal(self, bot, update):
        update.message.reply_text(not_yet_in_production)
