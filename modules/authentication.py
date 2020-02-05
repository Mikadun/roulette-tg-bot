from modules.mail import verification_mail
from modules.db_manager import unauth_users, auth_users
from random import randint

def send_code(user_id, email):
    MIN, MAX = 1000, 9999
    code = randint(MIN, MAX)
    unauth_users.update_email(user_id, email, code)
    verification_mail(email, code)

def check_code(user_id, code):
    try:
        if unauth_users.get_code(user_id) == int(code):
            unauth_users.next_state(user_id)
            return True
    except:
        return False

def start_registration(user_id):
    return not auth_users.check_user_id(user_id) and unauth_users.add(user_id)

def add_full_name(user_id, full_name):
    unauth_users.update_name(user_id, full_name[1], full_name[2], full_name[0])

def register(user_id, group):
    info = unauth_users.get_info(user_id)
    auth_users.add(*info[1:5], group, info[6])
    unauth_users.delete(user_id)

#unauth_users.clear()
#auth_users.clear()