
#!/usr/bin/python

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, \
    RegexHandler
from secrets import *
import logging
import os
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
from urllib2 import urlopen
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

temperature_button = u"\U0001F321" + "Temperature"
get_status_button = u"\U0001F49A" + "Get Status"
set_status_button = u"\U0001F9E1" + "Set Status"
enable_hurt_button = u"\U0001F494" + "Enable Hurt"
disable_hurt_button = u"\U00002764" + "Disable Hurt"
wallet_button = u"\U0001F4B0" + "Wallet"
daily_zeit_button = u"\U0000231A" + "Daily Zeit"
get_photo_button = u"\U0001F4F8" + "Get Photo"
day_deal_button = u"\U0001F4B9" + "Day Deal"
week_deal_button = u"\U0001F911" + "Week Deal"
german_button = u"\U0001F468" + "German"
digitec_deal_button = u"\U0001F4BB" + "Digitec Deal"

back_button = u"\U0001F448" + " Back"
next_button = u"\U0001F449" + " Next"

not_enough_permissions = "You are not authorized"
not_yet_in_production = "I'm sorry but this feature is not yet in production"


def start(bot, update):
    update.message.reply_text('Hi! I\'m SepphoBot!!!')


def command_list(bot, update):
    commands_string = ""
    for command, description in commands.items():
        commands_string = commands_string + command + ' - ' + description + '\n'
    update.message.reply_text(commands_string)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def getCostMin(bot, update):
    notWorksYet(bot, update)


def day_deal_menu(bot, update, user_data):
    dayDeal(bot, update)


def dayDeal(bot, update):
    update.message.reply_markdown("[Look for the daily deal!](https://www.daydeal.ch/).")


def week_deal_menu(bot, update, user_data):
    weekDeal(bot, update)


def weekDeal(bot, update):
    update.message.reply_markdown("[Look for the weekly deal!](https://www.daydeal.ch/deal-of-the-week).")


def digitec_deal_menu(bot, update, user_data):
    digitecDeal(bot, update)


def digitecDeal(bot, update):
    notWorksYet(bot, update)


def daily_zeit_menu(bot, update, user_data):
    dailyZeit(bot, update)


def dailyZeit(bot, update):
    notWorksYet(bot, update)


def get_photo_menu(bot, update, user_data):
    getPhoto(bot, update)


def getPhoto(bot, update):
    notWorksYet(bot, update)


def wallet_menu(bot, update, user_data):
    wallet(bot, update)


def wallet(bot, update):
    notWorksYet(bot, update)


def german_menu(bot, update, user_data):
    german(bot, update)


def german(bot, update):
    notWorksYet(bot, update)


def startMenu(bot, update):
    keyboard2 = [
        [KeyboardButton(text=temperature_button), KeyboardButton(text=get_status_button),
         KeyboardButton(text=set_status_button)],
        [KeyboardButton(text=enable_hurt_button), KeyboardButton(text=disable_hurt_button),
         KeyboardButton(text=next_button)]
    ]

    physical_reply_markup = ReplyKeyboardMarkup(keyboard=keyboard2)
    bot.sendMessage(update.message.chat_id, text="Page zero", reply_markup=physical_reply_markup)
    return START_MENU_RESULT


def second_page(bot, update, user_data):
    keyboard3 = [
        [KeyboardButton(text=wallet_button), KeyboardButton(text=daily_zeit_button),
         KeyboardButton(text=get_photo_button)],
        [KeyboardButton(text=back_button), KeyboardButton(text=day_deal_button),
         KeyboardButton(text=next_button)]
    ]
    physical_reply_markup = ReplyKeyboardMarkup(keyboard=keyboard3)
    bot.sendMessage(update.message.chat_id, text="Page one", reply_markup=physical_reply_markup)

    return SECOND_PAGE_RESULT


def third_page(bot, update, user_data):
    keyboard4 = [[KeyboardButton(text=week_deal_button), KeyboardButton(text=german_button)],
                 [KeyboardButton(text=back_button), KeyboardButton(text=digitec_deal_button)]]

    physical_reply_markup = ReplyKeyboardMarkup(keyboard=keyboard4)
    bot.sendMessage(update.message.chat_id, text="Page two", reply_markup=physical_reply_markup)
    return THIRD_PAGE_RESULT


def exitKeyboard(bot, update):
    bot.sendMessage(update.message.chat_id, 'Deleting keyboard', reply_markup=ReplyKeyboardRemove())


FIRST, SECOND = range(2)
# START_MENU_RESULT, SECOND_PAGE_RESULT = range(2)
START_MENU_RESULT, SECOND_PAGE_RESULT, THIRD_PAGE_RESULT = range(3)


def menuTest(bot, update):
    keyboard = [
        [InlineKeyboardButton(u"Next", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        u"Start handler, Press next",
        reply_markup=reply_markup
    )
    return FIRST


def first(bot, update):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(u"Next", callback_data=str(SECOND))]
    ]
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"First CallbackQueryHandler, Press next"
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return SECOND


def second(bot, update):
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"Second CallbackQueryHandler"
    )
    return


def get_temperature_menu(bot, update, user_data):
    getTemperature(bot, update)


def getTemperature(bot, update):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # enable GPIO4 for the temperature sensor
    GPIO.setup(4, GPIO.OUT)

    # read data from DHT11 connected at GPIO4
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    text = "- Temperature is around " + str(temperature) + " C " + "\n" + "- Humidity is around " + str(humidity) + ""
    update.message.reply_text(text)


def getAutoBit():
    if (os.path.isfile('/tmp/autobit')):
        fp = open('/tmp/autobit', 'r')
        if (fp.read() == '1'):
            returnValue = "AUTO"
        else:
            returnValue = "MANUAL"
        fp.close()
        return returnValue
    else:
        fp = open('/tmp/autobit', 'a').close()
        return "Manual"


def setAutoBit(bit):
    if (os.path.isfile('/tmp/autobit')):
        fp = open('/tmp/autobit', 'w')
    else:
        fp = open('/tmp/autobit', 'a')

    fp.write(str(bit))
    fp.close()


def isAuthorized(bot, update):
    id_user = update.message.from_user.id
    if (int(id_user) != int(sepphobot_auth_id)):
        return False
    return True


def get_status_menu(bot, update, user_data):
    getStatus(bot, update)


def getStatus(bot, update):
    id_user = update.message.from_user.id
    int(id_user)
    if (isAuthorized(bot, update) == False):
        response = not_enough_permissions + " your ID is: " + id_user
    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        response = ""

        # check relay status
        try:
            relay_status = open("/tmp/autoPI.txt", "r").readline()
        except IOError:
            relay_status = -1
        relay_status = int(relay_status)
        my_ip = urlopen('http://ip.42.pl/raw').read()
        response += "IP address = " + str(my_ip) + "\n"
        response += "Mode: " + str(getAutoBit()) + "\n"
        if (relay_status == 1):
            response += "The relay is ON, Sir"
        elif (relay_status == -1):
            response += "The relay is UNKNOW, Sir"
        else:
            response += "The relay is OFF, Sir"
    update.message.reply_text(response)


def isAuthorized(bot, update):
    id_user = update.message.from_user.id
    if (int(id_user) != int(sepphobot_auth_id)):
        return False
    return True
    update.message.reply_text(response)


def set_status_menu(bot, update, user_data):
    setStatus(bot, update)


def setStatus(bot, update):
    response = ""
    if (isAuthorized(bot, update) == False):
        response = not_enough_permissions
    command = "" + update.message.text
    command = str(command[11:])
    command = command.upper()
    # print len(command) , " - " , command
    if (len(command) > 0):
        if (command == "AUTO"):
            setAutoBit(1)
            response = "Mode setted to AUTO"
        elif (command == "MANUAL"):
            setAutoBit(0)
            response = "Mode setted to MANUAL"
    else:
        response = "Nothing to do here"
    update.message.reply_text(response)


stopHurt = 0


def disable_hurt_menu(bot, update, user_data):
    disableHurt(bot, update)


def disableHurt(bot, update):
    global stopHurt
    response = ""
    if (isAuthorized(bot, update) == False):
        response = not_enough_permissions
    else:
        stopHurt = 1
        response = "Stopping Hurt system..."
    update.message.reply_text(response)


def enable_hurt_menu(bot, update, user_data):
    enableHurt(bot, update)


def enableHurt(bot, update):
    global stopHurt
    response = ""
    if (isAuthorized(bot, update) == False):
        response = not_enough_permissions
    else:
        stopHurt = 0
        response = "Restarting Hurt system..."
    update.message.reply_text(response)


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


def notWorksYet(bot, update):
    update.message.reply_text(not_yet_in_production)


def contrib(bot, update):
    update.message.reply_text("You can help at https://github.com/mfalz/sepphobot")


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


def main():
    updater = Updater(sepphobot_telegram_token)
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('menuTest', menuTest)],
    #     states={
    #         FIRST: [CallbackQueryHandler(first)],
    #         SECOND: [CallbackQueryHandler(second)]
    #     },
    #     fallbacks=[CommandHandler('menuTest', menuTest)]
    # )

    init_menu_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('startMenu', startMenu)],
        states={
            START_MENU_RESULT: [RegexHandler('^' + temperature_button + '$',
                                             get_temperature_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + get_status_button + '$',
                                             get_status_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + set_status_button + '$',
                                             set_status_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + enable_hurt_button + '$',
                                             enable_hurt_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + disable_hurt_button + '$',
                                             disable_hurt_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + next_button + '$',
                                             second_page,
                                             pass_user_data=True),
                                RegexHandler('^' + back_button + '$',
                                             startMenu)
                                ],
            SECOND_PAGE_RESULT: [RegexHandler('^' + wallet_button + '$',
                                              wallet_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + daily_zeit_button + '$',
                                              daily_zeit_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + get_photo_button + '$',
                                              get_photo_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + day_deal_button + '$',
                                              day_deal_menu,
                                              pass_user_data=True),
                                 RegexHandler('^' + next_button + '$',
                                              third_page,
                                              pass_user_data=True),
                                 RegexHandler('^' + back_button + '$',
                                              startMenu)
                                 ],
            THIRD_PAGE_RESULT: [RegexHandler('^' + week_deal_button + '$',
                                             week_deal_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + german_button + '$',
                                             german_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + digitec_deal_button + '$',
                                             digitec_deal_menu,
                                             pass_user_data=True),
                                RegexHandler('^' + back_button + '$',
                                             second_page,
                                             pass_user_data=True)
                                ]
        },
        fallbacks=[CommandHandler('exitKeyboard', exitKeyboard)]
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(init_menu_conv_handler)
    # dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler(" ", command_list))
    dp.add_handler(CommandHandler("help", command_list))
    dp.add_handler(CommandHandler("contrib", contrib))

    # raspberry PI features
    dp.add_handler(CommandHandler("getTemperature", getTemperature))
    dp.add_handler(CommandHandler("getStatus", getStatus))
    dp.add_handler(CommandHandler("setStatus", setStatus))

    # funny features
    dp.add_handler(CommandHandler("hurt", hurt))
    dp.add_handler(CommandHandler("disableHurt", disableHurt))
    dp.add_handler(CommandHandler("enableHurt", enableHurt))
    dp.add_handler(CommandHandler("german", german))

    # wallet tracking
    dp.add_handler(CommandHandler("wallet", wallet))

    # zeit tracking
    dp.add_handler(CommandHandler("dailyZeit", dailyZeit))
    # nas features
    dp.add_handler(CommandHandler("getPhoto", getPhoto))

    # AWS features

    # daily deals and product tracking
    dp.add_handler(CommandHandler("dayDeal", dayDeal))
    dp.add_handler(CommandHandler("weekDeal", weekDeal))
    dp.add_handler(CommandHandler("digitecDeal", digitecDeal))
    # news tracking

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()