import telebot
import os
from flask import Flask, request

APP_NAME = os.getenv('HEROKU_APP_NAME')
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Hello')

print('Bot is running')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook("https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
	return "!", 200

if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))