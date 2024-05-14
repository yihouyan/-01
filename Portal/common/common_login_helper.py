#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-2-6
# software: PyCharm



from functools import wraps
from os import abort
from flask import request, g

from utils.auth_helper import Auth


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_key = Auth.identify(request)
        if user_key > 0:
            g.user_key = user_key
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def login_super(func):
    @wraps(func)
    def wrapper():
        if g.user_key != 1:
            abort(403)
        return func()

    return wrapper
