from modules.db_roulettes.py import russian_roulette
from random import randint

def russian_roulette_start(reference_id, magazine = 6, misfire = 0):
    bullet = randint(1, magazine)
    return russian_roulette.add(reference_id, magazine, bullet, misfire)

def russian_roulette_shoot(reference_id):
    is_bullet, misfire = russian_roulette.get_info(reference_id)

    return is_bullet and not misfire < randint(0, 100)
