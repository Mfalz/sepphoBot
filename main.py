from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

# command dictionary
commands = {
'/':"command list", 
'/help':"the same of /",
'/getTemperature':"return temperature from DHT11 sensor", 
'/getStatus':"return the bot status [only Authorized users]",
'/setStatus active | passive':" - The bot automatically manages room temperature in active mode [only authorized users]"
}

def start(bot, update):
	update.message.reply_text('Hi! I\m SepphoBot!')

def command_list(bot,update):
	commands_string=""
	for command,description in commands.items():
		commands_string = commands_string + command + ' - ' + description + '\n'
	update.message.reply_text(commands_string)	

def echo(bot, update):
	update.message.reply_text(update.message.text)

def getTemperature(bot,update):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	# enable GPIO4 for the temperature sensor
	GPIO.setup(4,GPIO.OUT)

	# read data from DHT11 connected at GPIO4
	humidity,temperature=Adafruit_DHT.read_retry(11,4)	
	update.message.reply_text("The temperature is around " + str(temperature) + " C")

def getAutoBit():
	if(os.path.isfile('/tmp/autobit')):
		fp = open('/tmp/autobit','r')
		if(fp.read()=='1'):
			returnValue="ACTIVE"
		else: 
			returnValue="PASSIVE"
		fp.close()
		return returnValue
	else:
		fp = open('/tmp/autobit','a').close()
		return "Manual"
	
def setAutoBit(bit):
	if(os.path.isfile('/tmp/autobit')):
		fp = open('/tmp/autobit','w')
	else:
		fp = open('/tmp/autobit','a')
	
	fp.write(str(bit))
	fp.close()

def isAuthorized(bot,update):
	id_user = update.message.from_user.id
	if(int(id_user) != int(os.environ['mymaker'])):
		return False
	return True
	
def getStatus(bot,update):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	response = ""
	id_user = update.message.from_user.id
	print int(id_user)
	if(isAuthorized(bot,update) == False):
		response = "I'm sorry but I can answer only to my maker"	
	else:
		# check relay status
		GPIO.setup(18,GPIO.IN)
		relay_status=GPIO.input(18)			

		response += "Mode: " + str(getAutoBit()) + "\n"
		
		if(relay_status == 1):
			response+="The relay is ON, Sir"
		else:
			response+="The relay is OFF, Sir"
		update.message.reply_text(response)

def setStatus(bot,update):
	if(isAuthorized(bot,update) == False):
		update.message.reply_text("YOU SHALL NOT PASS!")
		return 0
	command = "" + update.message.text
	command = str(command[11:])
	command = command.upper()
	# print len(command) , " - " , command
	if(len(command) > 0):
		if(command == "ACTIVE"):
			setAutoBit(1)
			update.message.reply_text("Mode setted to ACTIVE")
		elif(command == "PASSIVE"):
			setAutoBit(0)
			update.message.reply_text("Mode setted to PASSIVE")

def notWorksYet(bot,update):
	update.message.reply_text("I'm sorry but this feature is not yet in production")


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	updater = Updater(os.environ['prod_sepphobot'])

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

    	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("",command_list))
	dp.add_handler(CommandHandler("help",command_list))
	dp.add_handler(CommandHandler("getTemperature",getTemperature))
	dp.add_handler(CommandHandler("getStatus",getStatus))
	dp.add_handler(CommandHandler("setStatus",setStatus))
	
	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

    	updater.idle()

if __name__ == '__main__':
	main()
