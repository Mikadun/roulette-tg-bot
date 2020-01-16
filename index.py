import telebot
import os

from modules import utils, authentication
from modules.states import States, states

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(func = states.is_current_state(states.S_ENTER_MAIL))
def got_email(message):
    if utils.is_fefu_email(message.text):
        if authentication.send_code(message.text, message.from_user.id) == -1:
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
        bot.send_message(message.chat.id, 'Wrong code')

@bot.message_handler(func = states.is_current_state(states.S_ENTER_GROUP))
def got_group(message):
    if authentication.check_group(message.from_user.id, message.text):
        register(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Succesfully registered')
    else:
        bot.send_message(message.chat.id, 'Group not found')

print('Bot is running')
bot.polling()