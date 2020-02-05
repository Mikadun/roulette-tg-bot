import telebot
import os
from flask import Flask, request
from modules import utils, authentication
from modules.states import states
from modules.db_manager import unauth_users
from modules import roulettes
from modules.db_admin_list import admin_list

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    if authentication.start_registration(message.from_user.id):
        bot.send_message(message.chat.id, 'Write your fefu email to register')
    else:
        bot.send_message(message.chat.id, 'You have been already registered or started registration')

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

@bot.message_handler(commands=['chose'])
def chose_line(message):
	try:
		text = message.text.split('\n')[1:]
		bot.send_message(message.chat.id, roulettes.chose_line(text))
	except:
		bot.send_message(message.chat.id, 'Invalid command. Must have lines below command')

@bot.message_handler(commands=['random'])
def random_ab(message):
	try:
		a, b = map(int, message.text.split()[1:])
		bot.send_message(message.chat.id, 'Result: {}'.format(roulettes.random(a, b)))
	except:
		bot.send_message(message.chat.id, 'Invalid command')

@bot.message_handler(commands=['admin'])
def admin_panel(message):
	try:
		if message.chat.type == "private":
			if admin_list.check(message.from_user.id):
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				markup.add('1', '2') #Имена кнопок
				msg = bot.reply_to(message, 'Test text', reply_markup=markup)
				bot.register_next_step_handler(msg, process_step)




			else:
				bot.send_message(message.chat.id, "You aren't admin, so f*** off")
		else:
			bot.send_message(message.chat.id, 'Admin panel work only in private chat')
	except:

@bot.message_handler(func = states.is_current_state(states.S_ENTER_MAIL))
def got_email(message):
    if utils.is_fefu_email(message.text):
        if authentication.send_code(message.from_user.id, message.text) == -1:
            bot.send_message(message.chat.id, 'This email was already registered')
        else:
            bot.send_message(message.chat.id, 'Send code to {}. Write your auth code from email'.format(message.text))
    else:
        bot.send_message(message.chat.id, 'Invalid email, try again')


@bot.message_handler(func = states.is_current_state(states.S_ENTER_CODE))
def got_code(message):
    if authentication.check_code(message.from_user.id, message.text):
        bot.send_message(message.chat.id, 'Write your full name in format: Last First Middle')
    else:
        bot.send_message(message.chat.id, 'Wrong code')

@bot.message_handler(func = states.is_current_state(states.S_ENTER_FULLNAME))
def got_full_name(message):
    full_name = utils.is_full_name(message.text)
    if full_name:
        authentication.add_full_name(message.from_user.id, full_name)
        bot.send_message(message.chat.id, 'Write you group')
    else:
        bot.send_message(message.chat.id, 'Invalid full name. Format: Last_name First_name Middle_name')

@bot.message_handler(func = states.is_current_state(states.S_ENTER_GROUP))
def got_group(message):
    if utils.check_group(message.text):
        authentication.register(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Succesfully registered')
    else:
        bot.send_message(message.chat.id, 'Group not found')

@bot.message_handler(func = lambda message: True)
def any_message(message):
    bot.send_message(message.chat.id, 'Write /help for command list')

if __name__ == "__main__":
    print('Bot is running')

    if os.getenv('DEV'):
        bot.remove_webhook()
        bot.infinity_polling()
    else:
        APP_NAME = os.getenv('HEROKU_APP_NAME')

        server = Flask(__name__)

        @server.route('/' + TOKEN, methods=['POST'])
        def get_message():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200

        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook("https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
            return "!", 200

        server.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
