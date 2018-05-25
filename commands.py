commands = {
    '' : {
        "info": "command list",
        "cmd":  "help"
    },
    'help' : {
        "info": "command list",
        "cmd":  "command_list"
    },
    'getTemperature' : {
        "info": "return temperature from DHT11 sensor",
        "cmd":  "sensor.getTemperature"
    },
    'getStatus' : {
        "info": "return the bot status [only Authorized users]",
        "cmd":  "sensor.getStatus"
    },
    'setStatus [auto|manual]' : {
        "info": "The bot automatically manages room temperature in active mode [only authorized users]",
        "cmd":  "sensor.setStatus"
    },
    'hurt' : {
        "info": "The bot chooses a random hurt sentences inspired to someone",
        "cmd":  "funny.hurt"
    },
    'dayDeal': {
        "info": "get daily deal from daydeal.ch",
        "cmd":"deal.dayDeal"
    },
    'digitecDeal': {
        "info":"get daily deal from digitec.ch",
        "cmd":"deal.digitecDeal"
    },
    'dailyZeit hh:ff jira-number': {
        "info":"set working hours for given jira task",
        "cmd":"zeit.dailyZeit"
    },
    'dailyZeit get [date]': {
        "info":"get working hours spents for each jira task in the date provided",
        "cmd":"help"
    },
    'getPhoto date': {
        "info":"return photos",
        "cmd":"nas.getPhoto"
    },
    'wallet show date': {
        "info":"",
        "cmd":"wallet.wallet"
    },
    'wallet [add | del] product price': {
        "info":"",
        "cmd":"help"
    },
    'weekDeal': {
        "info":"get weekly deal from daydeal.ch",
        "cmd":"deal.weekDeal"
    },
    'german [ level: A1|A2|B1|B2|C1 ]': {
        "info":"Return a random sentence",
        "cmd":"funny.german"
    },
    'contrib': {
        "info":"Contrib github url",
        "cmd":"contrib"
    }
}