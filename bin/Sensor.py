import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT

class Sensor:
    Secret = 0

    def __int__(self,secret):
        self.Secret=secret

    def getTemperature(self, bot, update):
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


    def setAutoBit(self, bit):
        if (os.path.isfile('/tmp/autobit')):
            fp = open('/tmp/autobit', 'w')
        else:
            fp = open('/tmp/autobit', 'a')

        fp.write(str(bit))
        fp.close()

    def getStatus(self, bot, update):
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

    def setStatus(self, bot, update):
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