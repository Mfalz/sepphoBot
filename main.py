#!/usr/bin/python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, \
    RegexHandler
import logging

from bin.utils.Constant import *
from bin.utils.Message import *
from bin.utils.Secret import *
from bin.utils.User import *
from bin.StartMenu import *

from bin.Deal import *
from bin.Funny import *
from bin.Sensor import *
from bin.Zeit import *
from bin.Wallet import *
from bin.Nas import *


def start(bot, update):
    update.message.reply_text('Hi! I\'m ChebbyBot!')


def contrib(bot, update):
    update.message.reply_text("You can help at https://github.com/mfalz/sepphoBot")


def error(bot, update, err):
    logger.warning('Update "%s" caused error "%s"' % (update, err))

# command dictionary


commands = {
    '/' : {
        "info": "command list",
        "cmd":  "help"
    },
    '/getTemperature' : {
        "info": "return temperature from DHT11 sensor",
        "cmd":  "sensor.getTemperature"
    },
    '/getStatus' : {
        "info": "return the bot status [only Authorized users]",
        "cmd":  "sensor.getStatus"
    },
    '/setStatus [auto|manual]' : {
        "info": "The bot automatically manages room temperature in active mode [only authorized users]",
        "cmd":  "sensor.setStatus"
    },
    '/hurt someone [--disable|--enable]' : {
        "info": "The bot chooses a random hurt sentences inspired to someone",
        "cmd":  "funny.hurt"
    },
    '/dayDeal': {
        "info": "get daily deal from daydeal.ch",
        "cmd":"deal.dayDeal"
    },
    '/digitecDeal': {
        "info":"get daily deal from digitec.ch",
        "cmd":"deal.digitecDeal"
    },
    '/dailyZeit hh:ff jira-number': {
        "info":"set working hours for given jira task",
        "cmd":"zeit.dailyZeit"
    },
    '/dailyZeit get [date]': {
        "info":"get working hours spents for each jira task in the date provided",
        "cmd":""
    },
    '/getPhoto date': {
        "info":"return photos",
        "cmd":"nas.getPhoto"
    },
    '/wallet show date': {
        "info":"",
        "cmd":"wallet.wallet"
    },
    '/wallet [add | del] product price': {
        "info":"",
        "cmd":""
    },
    '/weekDeal': {
        "info":"get weekly deal from daydeal.ch",
        "cmd":"deal.weekDeal"
    },
    '/german [ level: A1|A2|B1|B2|C1 ]': {
        "info":"Return a random sentence",
        "cmd":"funny.german"
    },
    '/contrib': {
        "info":"Contrib github url",
        "cmd":"contrib"
    }
}


def command_list(bot, update):
    commands_string = ""
    for command, description in commands.items():
        commands_string = commands_string + command + ' - ' + description + '\n'
    update.message.reply_text(commands_string)


def main():
    secret = Secret()
    updater = Updater(secret.getTelegramToken())
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    sensor = Sensor(secret)
    wallet = Wallet(secret)
    zeit = Zeit(secret)
    funny = Funny(secret)
    deal = Deal(secret)
    nas = Nas(secret)

    # create available commands list
    # for command in commands.item():
    #     dp.add_handler(CommandHandler("" + command, command))

    start_menu_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('startMenu', startMenu)],
        states={
            START_MENU_RESULT: [RegexHandler('^' + temperature_button + '$',
                                             sensor.get_temperature_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + get_status_button + '$',
                                             sensor.get_status_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + set_status_button + '$',
                                             sensor.set_status_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + enable_hurt_button + '$',
                                             funny.enable_hurt_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + disable_hurt_button + '$',
                                             funny.disable_hurt_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + next_button + '$',
                                             second_page,
                                             pass_user_data=True),
                                RegexHandler('^' + back_button + '$',
                                             startMenu)
                                ],
            SECOND_PAGE_RESULT: [RegexHandler('^' + wallet_button + '$',
                                              wallet.wallet_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + daily_zeit_button + '$',
                                              zeit.daily_zeit_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + get_photo_button + '$',
                                              nas.get_photo_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + day_deal_button + '$',
                                              deal.day_deal_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + next_button + '$',
                                              third_page,
                                              pass_user_data=True),
                                 RegexHandler('^' + back_button + '$',
                                              startMenu)
                                 ],
            THIRD_PAGE_RESULT: [RegexHandler('^' + week_deal_button + '$',
                                             deal.week_deal_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + german_button + '$',
                                             funny.german_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + digitec_deal_button + '$',
                                             deal.digitec_deal_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + back_button + '$',
                                             second_page,
                                             pass_user_data=True)
                                ]
        },
        fallbacks=[CommandHandler('exitKeyboard', exitKeyboard)]
    )

    dp.add_handler(start_menu_conv_handler)

    for command in commands:
        dp.add_handler(CommandHandler(command, command["cmd"]))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    main()
