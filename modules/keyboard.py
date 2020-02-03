import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 6
    buttons = [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 37)]
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("Even", callback_data="Even"),
               InlineKeyboardButton("Odd", callback_data="Odd")
               )
    markup.add(InlineKeyboardButton("Red", callback_data="Red"),
               InlineKeyboardButton("Black", callback_data="Black")
               )
    markup.add(InlineKeyboardButton("1-18", callback_data="1-18"),
               InlineKeyboardButton("19-36", callback_data="19-36")
               )
    return markup