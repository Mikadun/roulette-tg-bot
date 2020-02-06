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
		bot.send_message(message.chat.id, "Points was added")
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
		bot.send_message(message.chat.id, "Points was removed")
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
	elif message.text=="NO":
		bot.send_message(message.chat.id, "OK")
		admin_panel_main(message)
	else:
		bot.send_message(message.chat.id, "Invalid command")
		admin_panel_main(message)		