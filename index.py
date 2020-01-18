import telebot
import os
from modules import utils, authentication
from modules.states import states
from modules.db_manager import unauth_users

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
    if authentication.start_registration(message.from_user.id):
        bot.send_message(message.chat.id, 'Write your fefu email to register')
    else:
        bot.send_message(message.chat.id, 'You have been already registered or started registration')

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
        bot.send_message(message.chat.id, 'Write you group')
    else:
        bot.send_message(message.chat.id, 'Write your full name in format: Last First Middle')

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

print('Bot is running')
bot.polling()