import json
from modules.bot_db import email_confirmation as em_conf, users
from transliterate import translit

def get_token():
    file_path = 'telegram-token.json'
    try:
        return json.load(open(file_path))['token']
    except:
        print('Miss token file. Write your telegram bot token here')
        token = input()
        for c in [' ', '\n', '"', "'"]:
            token = token.strip(c)
        json.dump({'token': token}, open(file_path, 'w'))
        return get_token()

def is_fefu_email(message):
    email = message.text.strip()
    if users.check_user_id(message.from_user.id):
        return False

    if email.count('@dvfu.ru') + email.count('@students.dvfu.ru') == 1:
        email = email.split('@')[0]
        print(email)
        if email.count('.') + email.count('_') == 1:
            for i in range(len(email)):
                if (ord(email[i])<97 or ord(email[i])>122) and email[i]!='.' and email[i]!='_':
                    return False
            return True
    return False

STATES = {'expect_code': 0, 'expect_group': 1}
def is_code(message):
    if not em_conf.get_state(message.from_user.id) == STATES['expect_code']:
        return False

    text = message.text
    return text.isnumeric() and 1000 <= int(text) <= 9999

def is_group(message):
    if not em_conf.get_state(message.from_user.id) == STATES['expect_group']:
        return False
    
    return True

def get_name(email):
    left_part = email.split('@')[0]
    dividers = ['.', '_']

    for divider in dividers:
        if divider in left_part:
            name = ' '.join(left_part.split(divider))
            return translit(name, language_code='ru', reversed=True)

    return translit(left_part, language_code='ru', reversed=True)

def get_info(user_id):
    result = users.get_info(user_id)
    if result == -1:
        return "You're not registered"
    else:
        id, tg_id, name, group, score, email = result
        return ' '.join((str(i).strip() for i in result))

if __name__ == '__main__':
    print(get_token())