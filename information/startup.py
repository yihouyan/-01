#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-1-12
# software: PyCharm




import fire
from tornado.options import define
from websdk.program import MainProgram
from settings import settings as app_settings
from biz.applications import Application as CmdbApp
from biz.crontab_app import Application as CronApp

define("service", default='api', help="start service flag", type=str)


class MyProgram(MainProgram):
    def __init__(self, service='cmdb_api', progressid=''):
        self.__app = None
        settings = app_settings
        if service == 'cmdb':
            self.__app = CmdbApp(**settings)
        elif service == 'cmdb_cron':
            self.__app = CronApp(**settings)
        super(MyProgram, self).__init__(progressid)
        self.__app.start_server()


if __name__ == '__main__':
    fire.Fire(MyProgram)

"""
python3 startup.py --service='cmdb' --port=8055

python3 startup.py --service='cmdb_cron'


"""
