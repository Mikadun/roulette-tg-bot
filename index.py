import telebot
import os
from modules.db_admin_list import admin_list
from modules.db_roulettes import roulette
#from modules.roulettes import f_roulette

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
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Something going wrong...")

#@bot.message_handler(commands=['participate'])
#def first_roulette_participate(message):


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