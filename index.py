import telebot

import os
from modules.db_roulettes import Classic_roulette

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['bet'])
def classic_roulette_bet(message):
    try:
        data = message.text.split()
        Classic_roulette().add(message.chat.id, message.from_user.id, data[0], data[1])
    except:
        bot.send_message(message.chat.id, 'Wrong command/')

print('Bot is running')
bot.polling()