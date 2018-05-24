import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import os
from urllib2 import urlopen
from .utils.Constant import *


class Sensor:
    Secret = 0

    def __init__(self, secret):
        self.Secret = secret

    def get_temperature_menu(self, bot, update, user_data):
        self.getTemperature(bot, update)

    def getTemperature(self, bot, update):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # enable GPIO4 for the temperature sensor
        GPIO.setup(4, GPIO.OUT)

        # read data from DHT11 connected at GPIO4
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        text = "- Temperature is around " + str(temperature) + " C " + "\n" + "- Humidity is around " + str(
            humidity) + ""
        update.message.reply_text(text)

    def getAutoBit(self):
        if os.path.isfile('/tmp/autobit'):
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

    def setAutoBit(self, bit):
        if (os.path.isfile('/tmp/autobit')):
            fp = open('/tmp/autobit', 'w')
        else:
            fp = open('/tmp/autobit', 'a')

        fp.write(str(bit))
        fp.close()

    def get_status_menu(self, bot, update, user_data):
        self.getStatus(bot, update)

    def getStatus(self, bot, update):
        id_user = update.message.from_user.id
        int(id_user)
        if not self.Secret.isAuthorized(bot, update):
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
            response += "Mode: " + str(self.getAutoBit()) + "\n"
            if (relay_status == 1):
                response += "The relay is ON, Sir"
            elif (relay_status == -1):
                response += "The relay is UNKNOW, Sir"
            else:
                response += "The relay is OFF, Sir"
        update.message.reply_text(response)

    def set_status_menu(self, bot, update, user_data):
        self.setStatus(bot, update)

    def setStatus(self, bot, update):
        response = ""
        if not self.Secret.isAuthorized(bot, update):
            response = not_enough_permissions
        command = "" + update.message.text
        command = str(command[11:])
        command = command.upper()
        # print len(command) , " - " , command
        if len(command) > 0:
            if command == "AUTO":
                self.setAutoBit(1)
                response = "Mode setted to AUTO"
            elif command == "MANUAL":
                self.setAutoBit(0)
                response = "Mode setted to MANUAL"
        else:
            response = "Nothing to do here"
        update.message.reply_text(response)
