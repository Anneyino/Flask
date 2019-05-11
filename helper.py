import random
import database


def generate_session_id():
    return '{:090x}'.format(random.randrange(16 ** 90))


def user_init(uid):
    database.insert_init_user_helper(uid)
    database.insert_init_user_subject(uid)
