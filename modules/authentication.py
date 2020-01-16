from modules.mail import verification_mail
from modules.db_manager import unauth_users, auth_users
from random import randint

def send_code(receiver, user_id):
    MIN, MAX = 1000, 9999
    code = randint(MIN, MAX)
    if unauth_users.add(receiver, code, user_id) == -1:
        return -1
    print(unauth_users.show_all())
    verification_mail(receiver, code)

def check_code(user_id, code):
    if unauth_users.get_code(user_id) == code:
        unauth_users.set_state(user_id)
        return True
    return False

def register(user_id, group):
    email = unauth_users.get_email(user_id)
    auth_users.add(get_name(email), email, group, user_id)
    unauth_users.delete(user_id)

