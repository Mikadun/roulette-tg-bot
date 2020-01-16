import telebot
from modules.utils import getToken

bot = telebot.TeleBot(token = getToken())

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Hello')

print('Bot is running')
bot.polling()