class Funny:
    Secrets = 0
    update = 0
    def __init__(self,secrets,update):
        self.Secrets = secrets
        self.update = update


    def disableHurt(self):
        if self.Secrets.isAuthorized():
            update.message.reply_text("Stopping Hurt system...")

    def enableHurt(bot, update):
        global stopHurt
        if (isAuthorized(bot, update) == False):
            return
        stopHurt = 0
        update.message.reply_text("Restarting Hurt system...")


    def hurt(bot, update):
        global stopHurt
        if (stopHurt == 1):
            update.message.reply_text("Hurt system is stopped")
            return
        who = "" + update.message.text
        who = str(who[5:])
        if (len(who) > 0 and len(who) < 14):
            sentences = open("/opt/hurtSentences.txt", "r").read().splitlines()
            aSentence = random.choice(sentences)
            update.message.reply_text("Questa la dedico a " + who + "\n" + aSentence)

    def german(bot, update):
        print("Generate a random sentence in German")