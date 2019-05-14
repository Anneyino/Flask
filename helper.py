import random
import databaseq


def generate_session_id():
    return '{:090x}'.format(random.randrange(16 ** 90))


def user_init(uid):
    databaseq.insert_init_user_helper(uid)
    databaseq.insert_init_user_subject(uid)


def check_login(username, passwd):
    currect_passwd = databaseq.get_password(username)
    if not currect_passwd:
        return False
    return currect_passwd == passwd
