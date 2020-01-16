from enum import Enum

class States(Enum):
        S_DEFAULT = 0
        S_ENTER_MAIL = 1
        S_ENTER_CODE = 2
        S_ENTER_FULLNAME = 3
        S_ENTER_GROUP = 4

states = States()
