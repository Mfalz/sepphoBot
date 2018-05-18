#!/usr/bin/python

from telegram.ext import Updater, CommandHandler
import logging

from utils import *
from Deal import *
from Funny import *
# from Sensor import *
from Zeit import *
from Wallet import *
from Nas import *

def start(bot, update):
    update.message.reply_text('Hi! I\m ChebbyBot!')

def getStatus(bot, update):
    print("Status")

def contrib(bot, update):
    update.message.reply_text("You can help at https://github.com/mfalz/chabbyBot")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

# command dictionary
commands = {
    '/': "command list",
    '/help': "the same of /",
    '/getTemperature': "return temperature from DHT11 sensor",
    '/getStatus': "return the bot status [only Authorized users]",
    '/setStatus [auto | manual]': " - The bot automatically manages room temperature in active mode [only authorized users]",
    '/hurt someone [--disable|--enable]': " - The bot chooses a random hurt sentences inspired to someone",
    '/dayDeal': "get daily deal from daydeal.ch",
    '/digitecDeal': "get daily deal from digitec.ch",
    '/dailyZeit hh:ff jira-number': "set working hours for given jira task",
    '/dailyZeit get [date]': "get working hours spents for each jira task in the date provided",
    '/getPhoto date': "return photos",
    '/wallet show date': "",
    '/wallet [add | del] product price': "",
    '/weekDeal': "get weekly deal from daydeal.ch",
    '/german [ level: A1|A2|B1|B2|C1 ]': "Return a random sentence",
    '/contrib': " - Contrib github url"
}

def command_list(bot, update):
    commands_string = ""
    for command, description in commands.items():
        commands_string = commands_string + command + ' - ' + description + '\n'
    update.message.reply_text(commands_string)

def main():
    secret = Secret
    updater = Updater(secret.getTelegramToken())
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # TODO. Lazy solution, How Does Dependency Injection work in python??
    # sensor = Sensor(secrets,updater)
    wallet = Wallet(secret,updater)
    zeit = Zeit(secret,updater)
    funny = Funny(secret,updater)
    deal = Deal(secret,updater)
    nas = Nas(secret,updater)
    funny.disableHurt(secret,updater)

    # create available commands list
    # for command in commands.item():
    #     dp.add_handler(CommandHandler("" + command, command))

    dp.add_handler(CommandHandler("start", secret.setUser))
    dp.add_handler(CommandHandler("", command_list))
    dp.add_handler(CommandHandler("help", command_list))
    dp.add_handler(CommandHandler("contrib", contrib))

    # raspberry PI features
    # dp.add_handler(CommandHandler("getTemperature", sensor.getTemperature))
    # dp.add_handler(CommandHandler("getStatus", sensor.getStatus))
    # dp.add_handler(CommandHandler("setStatus", sensor.setStatus))

    # funny features
    dp.add_handler(CommandHandler("hurt", funny.hurt))
    dp.add_handler(CommandHandler("disableHurt", funny.disableHurt))
    dp.add_handler(CommandHandler("enableHurt", funny.enableHurt))
    dp.add_handler(CommandHandler("german", funny.german))

    # wallet tracking
    dp.add_handler(CommandHandler("wallet", wallet))

    # zeit tracking
    dp.add_handler(CommandHandler("dailyZeit", zeit.dailyZeit))
    # nas features
    dp.add_handler(CommandHandler("getPhoto", nas.getPhoto))

    # AWS features

    # daily deals and product tracking
    dp.add_handler(CommandHandler("dayDeal", deal.dayDeal))
    dp.add_handler(CommandHandler("weekDeal", deal.weekDeal))
    dp.add_handler(CommandHandler("digitecDeal", deal.digitecDeal))
    # news tracking

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    main()
