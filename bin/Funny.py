import random
from .utils.Constant import *


class Funny:
    Secret = 0
    enabled = True

    def __init__(self, secret):
        self.Secret = secret

    def disable_hurt_menu(self, bot, update, user_data):
        self.disableHurt(bot, update)

    def disableHurt(self, bot, update):
        global stopHurt
        response = ""
        if not self.Secret.isAuthorized(bot, update):
            response = not_enough_permissions
        else:
            stopHurt = 1
            response = "Stopping Hurt system..."
        update.message.reply_text(response)

    def enable_hurt_menu(self, bot, update, user_data):
        self.enableHurt(bot, update)

    def enableHurt(self, bot, update):
        global stopHurt
        response = ""
        if not self.Secret.isAuthorized(bot, update):
            response = not_enough_permissions
        else:
            stopHurt = 0
            response = "Restarting Hurt system..."
        update.message.reply_text(response)

    def hurt(bot, update):
        global stopHurt
        if stopHurt == 1:
            update.message.reply_text("Hurt system is stopped")
            return
        who = "" + update.message.text
        who = str(who[5:])
        if 0 < len(who) < 14:
            sentences = open("/opt/hurtSentences.txt", "r").read().splitlines()
            aSentence = random.choice(sentences)
            update.message.reply_text("Questa la dedico a " + who + "\n" + aSentence)

    def german_menu(self, bot, update, user_data):
        self.german(bot, update)

    def german(self, bot, update):
        update.message.reply_text(not_yet_in_production)
