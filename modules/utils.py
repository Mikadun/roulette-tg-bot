import json
from modules.db_manager import unauth_users, auth_users

def is_fefu_email(email):
    email = email.strip()
    if email.count('@dvfu.ru') + email.count('@students.dvfu.ru') == 1:
        email = email.split('@')[0]
        if email.count('.') + email.count('_') == 1:
            for i in range(len(email)):
                if (ord(email[i])<97 or ord(email[i])>122) and email[i]!='.' and email[i]!='_':
                    return False
            return True
    return False

def is_full_name(name):
    data = name.lower().title().split()
    if len(data) != 3:
        return False

    for i in data:
        if not i.isalpha():
            return False
    return data

with open('group_list.json', encoding='utf-8') as f:
    groups = json.load(f)['data']

def check_group(group):
    return group in groups