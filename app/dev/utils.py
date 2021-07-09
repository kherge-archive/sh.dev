import grp
import os
import pwd

def get_group_id():
    return os.getgid()

def get_group_name():
    return grp.getgrgid(os.getgid()).gr_name

def get_user_id():
    return os.getuid()

def get_user_name():
    return pwd.getpwuid(os.getuid()).pw_name

def memoize(func):
    """Memoizes the result of a function."""
    memos = {}

    def memoized(*args, **kwargs):
        key = hash((args, frozenset(kwargs.items())))

        if not key in memos:
            memos[key] = func(*args, **kwargs)

        return memos[key]

    return memoized