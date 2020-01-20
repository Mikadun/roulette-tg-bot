import telebot
from modules.utils import getToken
from modules import roulettes
import os

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['russian'])
def russian_roulette_start(message):
	try:
		data = map(int, message.text.split()[1:])
		if roulettes.russian_roulette_start(message.chat.id, *data):
			bot.send_message(message.chat.id, 'Russian roulette has begun! You can /roll to shoot')
		else:
			bot.send_message(message.chat.id, 'Russian roulette has already started')
	except:
		bot.send_message(message.chat.id, 'Invalid command')

@bot.message_handler(commands=['roll'])
def russian_roulette_shoot(message):
	result = roulettes.russian_roulette_shoot(message.chat.id)
	if not result == -1:
		user = '{} {}'.format(message.from_user.first_name, message.from_user.last_name)
		if not result:
			bot.send_message(message.chat.id, '{} is safe, woooh'.format(user))
		else:
			bot.send_message(message.chat.id, '{} has got shot, F'.format(user))
	else:
		bot.send_message(message.chat.id, "You haven't start roulette. Write /russian")

print('Bot is running')
bot.polling()