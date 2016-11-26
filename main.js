var telegram = require('telegram-bot-api');
var exec = require('child_process').exec;
var rpiDhtSensor = require('rpi-dht-sensor');
 
var dht = new rpiDhtSensor.DHT11(4);
var readout = dht.read();

function readTemperature(){return readout.temperature.toFixed(2);}
function readHumidity(){return readout.humidity.toFixed(2);}

/* Telegram api */
var api = new telegram({token: process.env.TOKEN_sepphoBot,updates: {enabled: true}});

api.on('message', function(message){
	// I've received a message
		
	// my commands
	var commands = new Array("/getTemperature","/getHumidity","/lightON","/lightOFF")
	var text = message.text
	if(text == '/'){
		// return the commands list
		var response=" "
		commands.forEach(function(element){
			response=response.concat(element)+"\n"
		});
	}else if(text == commands[0]){
		// return Temperature and humidity from sensors
		var response="Hi, we have " + readTemperature() + " celsius degree, the humidity value is around " + readHumidity() + "%"
	}else if(text=="/start"){
		// is a simple message
		response="Hi! My name is Seppho, I'm a simple bot in JS and I'm running on a RaspberryPI because my maker aim to improve his skills with home automation.\nYou can see my commands typing /"
	}
	
	if(response!="")	
		api.sendMessage({
			chat_id: message.chat.id,
			text: response
		})
});
 
api.on('inline.query', function(message){
	// Received inline text
});
 
api.on('inline.result', function(message){
	// Received chosen inline result
});
 
api.on('inline.callback.query', function(message){
	// New incoming callback query
});
 
api.on('edited.message', function(message){
	// Message that was edited
});
 
api.on('update', function(message){
	// Generic update object
	// Subscribe on it in case if you want to handle all possible
	// event types in one callback
});
