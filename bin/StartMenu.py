from .utils.Constant import *
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


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
