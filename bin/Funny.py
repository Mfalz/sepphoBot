class Funny:
    Secret = 0
    enabled = True
    def __init__(self,secret,update):
        self.Secret = secret


    def disableHurt(self, bot, update):
        if self.Secret.isAuthorized(update):
            self.enabled = False
            update.message.reply_text("Disabling Hurt system...")

    def enableHurt(self, bot, update):
        if self.Secret.isAuthorized(update):
            self.enabled = True
            update.message.reply_text("Enabling Hurt system...")

    def hurt(self, bot, update):

        if self.enabled == False:
            update.message.reply_text("Hurt system is stopped")
            return
        who = "" + update.message.text
        who = str(who[5:])
        if (len(who) > 0 and len(who) < 14):
            sentences = open("/opt/hurtSentences.txt", "r").read().splitlines()
            aSentence = random.choice(sentences)
            update.message.reply_text("Questa la dedico a " + who + "\n" + aSentence)

    def german(self, bot, update):
        print("Generate a random sentence in German")