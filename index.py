import telebot
import os
from modules.db_admin_list import admin_list
from modules.db_roulettes import roulette
from modules import roulettes

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['roulette'])
def first_roulette(message):
    try:
        if admin_list.check(message.from_user.id):
            temp = message.text.split('\n')
            if len(temp) > 1:
                roulette.add(message.chat.id, *temp[1:])
            else:
                roulette.add(message.chat.id)
            bot.send_message(message.chat.id, "Admin started roulette. To participate, enter /participate")
        else:
            bot.send_message(message.chat.id, "It's for admin only")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Something going wrong...")

@bot.message_handler(commands=['participate'])
def first_roulette_participate(message):
    try:
        user = '{} {}'.format(message.from_user.first_name, message.from_user.last_name)
        if roulette.check(message.chat.id):
            if not(message.chat.id in roulette.check_user(message.from_user.id)):
                roulette.add_user(message.chat.id, message.from_user.id, message.from_user.first_name, message.from_user.last_name)
                bot.send_message(message.chat.id, '{} in roulette'.format(user))
            else:
                bot.send_message(message.chat.id, "{} already in roulette".format(user))
        else:
            bot.send_message(message.chat.id, "Roulette not started in this chat")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Something going wrong...")

@bot.message_handler(commands=['rroll'])
def first_roulette_roll(message):
    try:
        if admin_list.check(message.from_user.id):
            if roulette.check(message.chat.id):
                users = roulette.get_users(message.chat.id)

                if len(users) >= 3:
                    temp = roulette.get_info(message.chat.id)
                    win, lose = roulettes.f_roulette(users)

                    temp_s = ""
                    for i in range(len(win)):
                        name = roulette.get_user(win[i])
                        if name != [] and name != False:
                            temp_s += temp[0].replace("#fio#", *name) + "\n"

                    if temp_s != "":
                        bot.send_message(message.chat.id, temp_s)

                    temp_s = ""
                    for i in range(len(lose)):
                        name = roulette.get_user(lose[i])
                        if name != [] and name != False:
                            name = list(name[0])
                            name[0] = name[0].strip()
                            name[1] = name[1].strip()
                            temp_s += temp[1].replace("#fio#", name[0]+" "+name[1]) + "\n"

                    roulette.delete(message.chat.id)
                    bot.send_message(message.chat.id, temp_s)
                else:
                    bot.send_message(message.chat.id, "Need 3 or more participants")
            else:
                bot.send_message(message.chat.id, "Roulette not started in this chat")
        else:
            bot.send_message(message.chat.id, "It's for admin only")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Something going wrong...")





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