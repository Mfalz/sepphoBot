class Message:
    def echo(self, bot, update):
        update.message.reply_text(update.message.text)
