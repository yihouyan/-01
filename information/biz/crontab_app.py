#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-12-10
# software: PyCharm




import tornado
from websdk.application import Application as myApplication
from biz.timed_program import tail_data as my_timed_program


class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        my_program_callback = tornado.ioloop.PeriodicCallback(my_timed_program, 3600000)  #1小时
        my_program_callback.start()
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
