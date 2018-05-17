#!/usr/bin/python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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


def start(bot, update):
    update.message.reply_text('Hi! I\m SepphoBot!')


def command_list(bot, update):
    commands_string = ""
    for command, description in commands.items():
        commands_string = commands_string + command + ' - ' + description + '\n'
    update.message.reply_text(commands_string)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def getCostMin(bot, update):
    notWorksYet(bot, update)


def dayDeal(bot, update):
    bot.reply_markdown("*bold* _italic_ `fixed width font` [link](https://www.daydeal.ch/).")


def digitecDeal(bot, update):
    notWorksYet(bot, update)


def dailyZeit(bot, update):
    notWorksYet(bot, update)


def getPhoto(bot, update):
    notWorksYet(bot, update)


def wallet(bot, update):
    notWorksYet(bot, update)


def german(bot, update):
    notWorksYet(bot, update)


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


def getStatus(bot, update):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    response = ""
    id_user = update.message.from_user.id
    print(int(id_user))
    if (isAuthorized(bot, update) == False):
        response = "I'm sorry but I can answer only to my maker"
    else:
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


def getStatus(bot, update):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    response = ""
    id_user = update.message.from_user.id
    print
    int(id_user)
    if (isAuthorized(bot, update) == False):
        response = "You are not authorized, your ID is: " + id_user
    else:
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


def setStatus(bot, update):
    if (isAuthorized(bot, update) == False):
        update.message.reply_text("I'm so sorry, you can't set status :c")
        return 0
    command = "" + update.message.text
    command = str(command[11:])
    command = command.upper()
    # print len(command) , " - " , command
    if (len(command) > 0):
        if (command == "AUTO"):
            setAutoBit(1)
            update.message.reply_text("Mode setted to AUTO")
        elif (command == "MANUAL"):
            setAutoBit(0)
            update.message.reply_text("Mode setted to MANUAL")
    else:
        print("Nothing to do here")


stopHurt = 0


def disableHurt(bot, update):
    global stopHurt
    if (isAuthorized(bot, update) == False):
        return
    stopHurt = 1
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


def notWorksYet(bot, update):
    update.message.reply_text("I'm sorry but this feature is not yet in production")


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
    '/german [ level: A1|A2|B1|B2|C1 ]': "Return a random sentence",
    '/contrib': " - Contrib github url"
}


def main():
    updater = Updater(sepphobot_telegram_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

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
    dp.add_handler(CommandHandler("digitecDeal", digitecDeal))
    # news tracking

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
