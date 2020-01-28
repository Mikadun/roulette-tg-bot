import telebot
import os

APP_NAME = os.getenv('APP_NAME')
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Hello')

print('Bot is running')

bot.set_webhook("https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
bot.polling()