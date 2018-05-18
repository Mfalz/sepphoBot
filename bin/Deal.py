class Deal:
    Secret = 0

    def __int__(self,secret):
        self.Secret=secret

    def getCostMin(self, bot, update):
        print ("Given a product, return minimum cost from camelcamelcamel")

    def dayDeal(self, bot, update):
        update.message.reply_markdown("[Look for the daily deal!](https://www.daydeal.ch/).")

    def weekDeal(self, bot, update):
        update.message.reply_markdown("[Look for the weekly deal!](https://www.daydeal.ch/deal-of-the-week).")

    def digitecDeal(self, bot, update):
        print ("Show the digitec Deal")