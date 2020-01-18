from modules.mail import verification_mail
from modules.db_manager import unauth_users, auth_users
from random import randint

def send_code(user_id, email):
    MIN, MAX = 1000, 9999
    code = randint(MIN, MAX)
    unauth_users.update_email(user_id, email)
    unauth_users.update_code(user_id, code)
    verification_mail(email, code)

def check_code(user_id, code):
    if unauth_users.get_code(user_id) == code:
        unauth_users.next_state(user_id)
        return True
    return False

def start_registration(user_id):
    if unauth_users.add(user_id) == -1:
        return False
    unauth_users.next_state(user_id)
    print(unauth_users.get_state(user_id))

def add_full_name(user_id, full_name):
    unauth_users.update_name(user_id, full_name[1], full_name[2], full_name[0])
    unauth_users.next_state(user_id)

def register(user_id, group):
    email = unauth_users.get_email(user_id)
    #auth_users.add(get_name(email), email, group, user_id)
    unauth_users.delete(user_id)

