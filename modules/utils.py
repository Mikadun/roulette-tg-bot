import json
from modules.db_manager import unauth_users, auth_users

def is_fefu_email(email):
    email = email.strip()
    if email.count('@dvfu.ru') + email.count('@students.dvfu.ru') == 1:
        email = email.split('@')[0]
        print(email)
        if email.count('.') + email.count('_') == 1:
            for i in range(len(email)):
                if (ord(email[i])<97 or ord(email[i])>122) and email[i]!='.' and email[i]!='_':
                    return False
            return True
    return False

def is_code(code):
    return code.isnumeric() and 1000 <= int(code) <= 9999

def is_group(message):
    return True

def is_full_name(name):
    data = name.split()
    if len(data) != 3:
        return False

    for i in data:
        if not i.isalpha():
            return False
    return data