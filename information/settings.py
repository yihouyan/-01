#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-1-2
# software: PyCharm



import os
from websdk.consts import const

ROOT_DIR = os.path.dirname(__file__)
debug = True
xsrf_cookies = False
expire_seconds = 365 * 24 * 60 * 60
cookie_secret = '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2X6TP1o/Vo='


DEFAULT_DB_DBHOST = os.getenv('DEFAULT_DB_DBHOST', '192.168.1.1')
DEFAULT_DB_DBPORT = os.getenv('DEFAULT_DB_DBPORT', '25')
DEFAULT_DB_DBUSER = os.getenv('DEFAULT_DB_DBUSER', 'admin')
DEFAULT_DB_DBPWD = os.getenv('DEFAULT_DB_DBPWD', '123456')
DEFAULT_DB_DBNAME = os.getenv('DEFAULT_DB_DBNAME', 'test')


READONLY_DB_DBHOST = os.getenv('READONLY_DB_DBHOST', '192.168.1.1')
READONLY_DB_DBPORT = os.getenv('READONLY_DB_DBPORT', '25')  
READONLY_DB_DBUSER = os.getenv('READONLY_DB_DBUSER', 'admin')  
READONLY_DB_DBPWD = os.getenv('READONLY_DB_DBPWD', '123456')  
READONLY_DB_DBNAME = os.getenv('READONLY_DB_DBNAME', 'test')


DEFAULT_REDIS_HOST = os.getenv('DEFAULT_REDIS_HOST', '192.168.1.1')  
DEFAULT_REDIS_PORT = os.getenv('DEFAULT_REDIS_PORT', '6379')  
DEFAULT_REDIS_DB = 8
DEFAULT_REDIS_AUTH = True
DEFAULT_REDIS_CHARSET = 'utf-8'
DEFAULT_REDIS_PASSWORD = os.getenv('DEFAULT_REDIS_PASSWORD', 'cWCVKJ7ZHAK122VbivUf')  

try:
    from local_settings import *
except:
    pass

AWS_EVENT_TO_EMAIL = '1845546376@139.com'

PUBLIC_KEY = '/root/.ssh/id_rsa.pub'  # 默认

WEB_TERMINAL = ''

CODO_TASK_DB_HOST = os.getenv('CODO_TASK_DB_HOST', '192.168.1.1')
CODO_TASK_DB_PORT = os.getenv('CODO_TASK_DB_PORT', '25')
CODO_TASK_DB_USER = os.getenv('CODO_TASK_DB_USER', 'admin')
CODO_TASK_DB_PWD = os.getenv('CODO_TASK_DB_PWD', '123456')
CODO_TASK_DB_DBNAME = os.getenv('CODO_TASK_DB_DBNAME', 'test')

CODO_TASK_DB_INFO = dict(
    host=CODO_TASK_DB_HOST,
    port=CODO_TASK_DB_PORT,
    user=CODO_TASK_DB_USER,
    passwd=CODO_TASK_DB_PWD,
    db=CODO_TASK_DB_DBNAME
)

settings = dict(
    debug=debug,
    xsrf_cookies=xsrf_cookies,
    cookie_secret=cookie_secret,
    expire_seconds=expire_seconds,
    app_name='codo_cmdb',
    databases={
        const.DEFAULT_DB_KEY: {
            const.DBHOST_KEY: DEFAULT_DB_DBHOST,
            const.DBPORT_KEY: DEFAULT_DB_DBPORT,
            const.DBUSER_KEY: DEFAULT_DB_DBUSER,
            const.DBPWD_KEY: DEFAULT_DB_DBPWD,
            const.DBNAME_KEY: DEFAULT_DB_DBNAME,
        },
        const.READONLY_DB_KEY: {
            const.DBHOST_KEY: READONLY_DB_DBHOST,
            const.DBPORT_KEY: READONLY_DB_DBPORT,
            const.DBUSER_KEY: READONLY_DB_DBUSER,
            const.DBPWD_KEY: READONLY_DB_DBPWD,
            const.DBNAME_KEY: READONLY_DB_DBNAME,
        }
    },
    redises={
        const.DEFAULT_RD_KEY: {
            const.RD_HOST_KEY: DEFAULT_REDIS_HOST,
            const.RD_PORT_KEY: DEFAULT_REDIS_PORT,
            const.RD_DB_KEY: DEFAULT_REDIS_DB,
            const.RD_AUTH_KEY: DEFAULT_REDIS_AUTH,
            const.RD_CHARSET_KEY: DEFAULT_REDIS_CHARSET,
            const.RD_PASSWORD_KEY: DEFAULT_REDIS_PASSWORD
        }
    }
)