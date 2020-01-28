import telebot
import os

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Hello')

print('Bot is running')
bot.polling()