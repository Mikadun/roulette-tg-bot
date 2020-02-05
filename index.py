import os
from flask import Flask, request
from modules import utils, authentication
from modules.states import states
from modules.db_manager import unauth_users
from modules.db_manager import auth_users
from modules import roulettes
from modules.db_admin_list import admin_list
import telebot
from telebot import types

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
def admin_panel_main(message):
	try:
		if message.chat.type == "private":
			if admin_list.check(message.from_user.id):
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

				markup.row('Список зарегестрированных пользователей')
				markup.row('Список зарегестрированных пользователей по группе')
				markup.row('Добавить очки', 'Отнять очки')
				markup.row('Информация о пользователе', 'Список групп')
				markup.row('Удалить пользователя')
				markup.row('Отключиться от панели админа')
				
				msg = bot.send_message(message.chat.id, 'Wait Your command, Admin', reply_markup=markup)

				bot.register_next_step_handler(msg, process_step)

			else:
				bot.send_message(message.chat.id, "You aren't admin, so f*** off")
		else:
			bot.send_message(message.chat.id, 'Admin panel work only in private chat')
	except Exception as err:
		print(err)

def process_step(message):
	if message.text=='Список групп':
		temp = [i[0] for i in auth_users.get_groups()]
		bot.send_message(message.chat.id, "\n".join(temp))
		admin_panel_main(message)
	elif message.text=='Список зарегестрированных пользователей':
		temp = auth_users.show_all()

		for i in temp:
			bot.send_message(message.chat.id, "TG ID: " + str(i[1]) + "\n Name: " + i[2].strip() + " " + i[3].strip() + " " + i[4].strip())

		admin_panel_main(message)
	elif message.text=='Список зарегестрированных пользователей по группе':
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		temp = [i[0] for i in auth_users.get_groups()]

		for i in temp:
			markup.row(i)

		msg = bot.send_message(message.chat.id, 'Choose group', reply_markup=markup)
		bot.register_next_step_handler(msg, admin_panel_users_by_group)
	elif message.text=='Информация о пользователе':
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		temp = auth_users.show_all()

		for i in temp:
			markup.row("TG ID: " + str(i[1]) + "\n Name: " + i[2].strip() + " " + i[3].strip() + " " + i[4].strip())

		msg = bot.send_message(message.chat.id, 'Choose user', reply_markup=markup)
		bot.register_next_step_handler(msg, admin_panel_user_info)
	elif message.text=='Добавить очки':
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		temp = auth_users.show_all()

		for i in temp:
			markup.row("TG ID: " + str(i[1]) + "\n Name: " + i[2].strip() + " " + i[3].strip() + " " + i[4].strip())

		msg = bot.send_message(message.chat.id, 'Choose user', reply_markup=markup)
		bot.register_next_step_handler(msg, admin_panel_add_points_1)
	elif message.text=='Отнять очки':
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		temp = auth_users.show_all()

		for i in temp:
			markup.row("TG ID: " + str(i[1]) + "\n Name: " + i[2].strip() + " " + i[3].strip() + " " + i[4].strip())

		msg = bot.send_message(message.chat.id, 'Choose user', reply_markup=markup)
		bot.register_next_step_handler(msg, admin_panel_remove_points_1)
	elif message.text=='Удалить пользователя':
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		temp = auth_users.show_all()

		for i in temp:
			markup.row("TG ID: " + str(i[1]) + "\n Name: " + i[2].strip() + " " + i[3].strip() + " " + i[4].strip())

		msg = bot.send_message(message.chat.id, 'Choose user', reply_markup=markup)
		bot.register_next_step_handler(msg, admin_panel_delete_user_1)
	elif message.text=='Отключиться от панели админа':
		bot.send_message(message.chat.id, "Bye, Admin")
		bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
	else:
		bot.send_message(message.chat.id, 'Invalid admin command')
		admin_panel_main(message)

def admin_panel_users_by_group(message):
	temp = auth_users.get_users_by_group(message.text)
	for i in temp:
		bot.send_message(message.chat.id, "TG ID: " + str(i[1]) + "\n Name: " + i[2].strip() + " " + i[3].strip() + " " + i[4].strip())
	admin_panel_main(message)

def admin_panel_user_info(message):
	temp = auth_users.get_info(int(message.text.split()[2]))
	bot.send_message(message.chat.id, "TG ID: " + str(temp[1]) + "\n Name: " + temp[2].strip() + " " + temp[3].strip() + " " + temp[4].strip()
						+ "\n Group: " + temp[5] + "\n Points: " + str(temp[6]) + "\n Email: " + temp[7])

	admin_panel_main(message)

def admin_panel_add_points_1(message):
	user_id = int(message.text.split()[2])

	msg = bot.send_message(message.chat.id, 'How many add?')

	bot.register_next_step_handler(msg, lambda m: admin_panel_add_points_2(m, user_id))

def admin_panel_add_points_2(message, user_id):
	try:
		if auth_users.check_user_id(user_id):
			auth_users.add_points(user_id, int(message.text))
		else:
			bot.send_message(message.chat.id, "Can't find this user")
			admin_panel_main(message)
	except:
		bot.send_message(message.chat.id, "Something going wrong")
		admin_panel_main(message)
	else:
		bot.send_message(message.chat.id, "OK")
		admin_panel_main(message)

def admin_panel_remove_points_1(message):
	user_id = int(message.text.split()[2])

	msg = bot.send_message(message.chat.id, 'How many remove?')

	bot.register_next_step_handler(msg, lambda m: admin_panel_remove_points_2(m, user_id))

def admin_panel_remove_points_2(message, user_id):
	try:
		if auth_users.check_user_id(user_id):
			auth_users.remove_points(user_id, int(message.text))
		else:
			bot.send_message(message.chat.id, "Can't find this user")
			admin_panel_main(message)
	except:
		bot.send_message(message.chat.id, "Something going wrong")
		admin_panel_main(message)
	else:
		bot.send_message(message.chat.id, "OK")
		admin_panel_main(message)

def admin_panel_delete_user_1(message):
	user_id = int(message.text.split()[2])

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

	markup.row("YES")
	markup.row("NO")

	msg = bot.send_message(message.chat.id, "You're goiung to delete this user: \n " + message.text + "\n ARE YOU SURE?", reply_markup=markup)

	bot.register_next_step_handler(msg, lambda m: admin_panel_delete_user_2(m, user_id))

def admin_panel_delete_user_2(message, user_id):
	if message.text=="YES":
		try:
			auth_users.delete(user_id)
		except:
			bot.send_message(message.chat.id, "Something going wrong")
			admin_panel_main(message)
		else:
			bot.send_message(message.chat.id, "User was deleted")
			admin_panel_main(message)
	else:
		bot.send_message(message.chat.id, "OK")
		admin_panel_main(message)

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
