class Message:
    def echo(bot, update):
        update.message.reply_text(update.message.text)