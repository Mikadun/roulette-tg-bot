import telebot
import os
from modules.db_admin_list import admin_list
from modules.db_roulettes import roulette
#from modules.roulettes import f_roulette

APP_NAME = os.getenv('APP_NAME')
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['roulette'])
def first_roulette(message):
    try:
        if admin_list.check(message.user.id):
            print(message.text.split())
            #roulette.add(message.chat.id)
            bot.send_message(message.chat.id, "Admin started roulette. To participate, enter /participate")
        else:
            bot.send_message(message.chat.id, "It's for admin only")
    except:
        bot.send_message(message.chat.id, "Something going wrong...")

#@bot.message_handler(commands=['participate'])
#def first_roulette_participate(message):


print('Bot is running')

bot.set_webhook("https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
bot.polling()