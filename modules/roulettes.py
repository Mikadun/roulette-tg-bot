from random import randint, choice
from secrets import choice
from index import bot


def f_roulette(players):
    n = len(players)

    win = set()
    lose = set()

    while len(win) < round(n/6):
        win.add(players[randint(0, n-1)])

    while len(lose) < int(n/3):
        r = randint(0, n-1)
        if not(players[r] in win):
            lose.add(players[r])

    return [list(win), list(lose)]

def chose_line(text):
    return choice(text)

def random(A, B):
    return randint(A, B)