from functools import wraps
import database
from flask import *
import sys


def show_friends(uid_primary):
    result = True
    try:
        all_friends = database.fetchAllres(
            "SELECT uid_secondary FROM friend WHERE uid_primary ='{}';".format(uid_primary))
    except:
        result = False
    return all_friends


POSSIBLE_SERVER_NAMES = [
    'https://moelearn.com/'
]


def is_valid_referer(referer):
    return any(referer.startswith(name) for name in POSSIBLE_SERVER_NAMES)


def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        referer = request.headers.get('Referer')
        if referer and not is_valid_referer(referer):
            print('Potential CSRF blocked', file=sys.stderr)
            return 'Potential CSRF blocked', 403
        return f(*args, **kwargs)

    return decorated_function
