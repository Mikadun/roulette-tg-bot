from enum import Enum
from modules.db_manager import unauth_users

class States(Enum):
        S_DONT_EXIST = -1
        S_DEFAULT = 0
        S_ENTER_MAIL = 1
        S_ENTER_CODE = 2
        S_ENTER_FULLNAME = 3
        S_ENTER_GROUP = 4

        def is_current_state(self, state):
                return (lambda message: States(unauth_users.get_state(message.from_user.id)) == state)

states = States(0)