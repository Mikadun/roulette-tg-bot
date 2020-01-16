from modules.mail import verification_mail
from modules.bot_db import email_confirmation, users
from modules.utils import get_name
from random import randint

def send_code(receiver, user_id):
    MIN, MAX = 1000, 9999
    code = randint(MIN, MAX)
    if email_confirmation.add(receiver, code, user_id) == -1:
        return -1
    print(email_confirmation.show_all())
    verification_mail(receiver, code)

def check_code(user_id, code):
    if email_confirmation.get_code(user_id) == code:
        email_confirmation.set_state(user_id)
        return True
    return False

def register(user_id, group):
    email = email_confirmation.get_email(user_id)
    users.add(get_name(email), email, group, user_id)
    email_confirmation.delete(user_id)

