import telebot

import os
from modules.db_roulettes import Classic_roulette
from modules.keyboard import gen_markup

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	bot.answer_callback_query(call.id, "You made a bet on "+call.data)
	#bot.send_message(call.message.chat.id, call.from_user.first_name+' '+call.from_user.last_name+' just made bet on '+call.data)

@bot.message_handler(commands=['bet'])
def message_handler(message):
	bot.send_message(message.chat.id, "Make your bet:", reply_markup=gen_markup())

print('Bot is running')
bot.polling()