#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-4-17
# software: PyCharm



from flask import Flask
from flask_cors import CORS


from api.resource import api
from utils.log_helper import init_log

from config import config, Config


def create_app(config_name):
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config['JSON_AS_ASCII'] = False


    init_log()
    api.init_app(app)
    return app