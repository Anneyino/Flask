import random


def generate_session_id():
    return '{:090x}'.format(random.randrange(16 ** 90))
