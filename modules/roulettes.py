from modules.db_roulettes import russian_roulette
from random import randint

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

russian_roulette.clear()