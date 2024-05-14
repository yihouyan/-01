#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2022-3-11
# software: PyCharm


import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



SECRET_KEY = 'ratn!684yf7ewt-%j%afwf7et9c=!oan$=w6#)fn#4u$ie4!as'

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    '192.168.1.1'
]


INSTALLED_APPS = (
    'viewflow.frontend',
    'viewflow',

    'material',
    'material.frontend',
    'material.admin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo.bloodtest',
    'demo.customnode',
    'demo.leave',
    'demo.hr',
    'demo.countersign',
    'demo.integration',
    'demo.employees',
    'demo.testing',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'material.frontend.middleware.SmoothNavigationMiddleware',
)

ROOT_URLCONF = 'demo.urls'

LOGIN_REDIRECT_URL = '/workflow/'

import dj_database_url  # NOQA

DATABASES = {
    'default': dj_database_url.config() or {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db{}{}.sqlite3'.format(*django.VERSION[:2])),
    }
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'demo/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'demo.website.users',
                'demo.website.testing_types',
                'material.frontend.context_processors.modules',
            ],
            'debug': True,
        },
    },
]


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if django.VERSION < (1, 7):
    INSTALLED_APPS += ('south', )


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "demo", "static"),
]

try:
    from demo.local_settings import *  # NOQA
except ImportError:
    pass