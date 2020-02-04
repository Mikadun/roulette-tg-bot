import telebot
import os
from flask import Flask, request
from modules import utils, authentication
from modules.states import states
from modules.db_manager import unauth_users

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

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

        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))