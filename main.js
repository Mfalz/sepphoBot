#!/usr/bin/env/node

var telegram = require('telegram-bot-api');
var exec = require('child_process').exec;
var rpiDhtSensor = require('rpi-dht-sensor');
 
/* Telegram api */
var api = new telegram({token: process.env.TOKEN_sepphoBot,
updates: {
        enabled: true,
        get_interval: 2000
    }
});

api.on('message', function(message){
	// I've received a message
	var response=new String()
	var commands = new Array("/getTemperature","/msg","/toggleLight")
	var text = message.text
		
	if(text == '/'){
		// return the commands list
		var response=" "
		commands.forEach(function(element){
			response=response.concat(element)+"\n"
		});
	}else if(text == commands[0]){
		var dht = new rpiDhtSensor.DHT11(4);
		var readout = dht.read();
		
		function readTemperature(){return readout.temperature.toFixed(2);}
		function readHumidity(){return readout.humidity.toFixed(2);}

		// return Temperature and humidity from sensors
		var response="Hi, we have " + readTemperature() + " celsius degree, the humidity value is around " + readHumidity() + "%"
	}else if(text.substr(0,4) == commands[1] && text.length>4){
		// forward message to me
		api.sendMessage({chat_id:process.env.maker_chat,text:text})
		
		var response="I sent " + text.substr(5,text.length) + " to my maker"
	}else if(text=="/start"){
		// is a simple message
		var response="Hi! My name is Seppho, I'm a simple bot in JS and I'm running on a RaspberryPI, that is because my maker aim to improve his skills with home automation.\nYou can see my commands typing /"
	}
	
	if(response.length>0)	
		api.sendMessage({
			chat_id: message.chat.id,
			text: response
		})
});
 
api.on('update', function(message){
	// Generic update object
	// Subscribe on it in case if you want to handle all possible
	// event types in one callback
});
