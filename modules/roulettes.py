from modules.db_roulettes import russian_roulette
from random import randint, choice
from secrets import choice

def classic(players):
    red, black = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36], []
    black = list(filter(lambda x: x not in red, range(0, 36)))
    x = randint(0, 36)
    print(x)
    res = {}
    res["x"] = x
    for i in players:
        print(i[1].strip())
        if res.get(i[0]) == None:
            res[i[0]] = 0
        if i[1].strip() == 'Even' and x%2 == 0:
            res[i[0]] += i[2]*2
        elif i[1].strip()  == 'Odd':
            res[i[0]] += i[2]*2
        elif i[1].strip()  == 'Red' and x in red:
            res[i[0]] += i[2]*2
        elif i[1].strip()  == 'Black' and x in black:
            res[i[0]] += i[2]*2
        elif i[1].strip()  == '1-18' and x<=18:
            res[i[0]] += i[2]*2
        elif i[1].strip()  == '19-36':
            res[i[0]] += i[2]*2
        elif int(i[1].strip()) == x:
            res[i[0]] += i[2]*36
    return res 

def russian_roulette_start(reference_id, magazine = 6, misfire = 0):
    bullet = randint(1, magazine)
    print('ref: {}, mag: {}, mis: {}, bul: {}'.format(reference_id, magazine, misfire, bullet))
    return russian_roulette.add(reference_id, magazine, bullet, misfire)

def russian_roulette_shoot(reference_id):
    result = russian_roulette.shoot(reference_id)
    print(result)
    if result:
        is_bullet, misfire = result
        return is_bullet and not misfire > randint(0, 100)
    else:
        return -1

def chose_line(text):
    return choice(text)

def random(A, B):
    return randint(A, B)

russian_roulette.clear()
