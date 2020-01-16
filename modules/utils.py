import json
from modules.db_manager import unauth_users, auth_users

def is_fefu_email(message):
    email = message.text.strip()
    if unauth_users.check_user_id(message.from_user.id):
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

def is_code(message):
    if not em_conf.get_state(message.from_user.id) == STATES['expect_code']:
        return False

    text = message.text
    return text.isnumeric() and 1000 <= int(text) <= 9999

def is_group(message):
    if not em_conf.get_state(message.from_user.id) == STATES['expect_group']:
        return False
    
    return True

def is_full_name(name):
        data = name.split()
        if len(data) != 3:
                return False
        for i in data:
                if not i.isalpha():
                        return False
        return data
    
def get_info(user_id):
    result = users.get_info(user_id)
    if result == -1:
        return "You're not registered"
    else:
        id, tg_id, name, group, score, email = result
        return ' '.join((str(i).strip() for i in result))

if __name__ == '__main__':
    print(get_token())