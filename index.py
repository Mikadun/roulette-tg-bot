import telebot
from modules.utils import getToken

bot = telebot.TeleBot(token = getToken())

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(func = is_fefu_email)
def got_email(message):
    if send_code(message.text, message.from_user.id) == -1:
        bot.send_message(message.chat.id, 'This tg account or email was already registered')
    else:
        bot.send_message(message.chat.id, 'Send code to {email}. Write your auth code'.format(email = message.text))

@bot.message_handler(func = is_code)
def got_code(message):
    code = int(message.text)
    if check_code(message.from_user.id, code):
        bot.send_message(message.chat.id, 'Write you group')
    else:
        bot.send_message(message.chat.id, 'Wrong code, try again')

@bot.message_handler(func = is_group)
def got_group(message):
    group = message.text
    register(message.from_user.id, group)
    bot.send_message(message.chat.id, 'Succesfully registered')

print('Bot is running')
bot.polling()