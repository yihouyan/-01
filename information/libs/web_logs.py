#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-8-25
# software: PyCharm


'''
Author : ss
date   : 2018-3-19
role   : web  log
'''

import logging
import os
import time
from shortuuid import uuid

log_fmt = ''.join(('PROGRESS:%(progress_id) -5s %(levelname) ', '-10s %(asctime)s %(name) -25s %(funcName) '
                                                                '-30s LINE.NO:%(lineno) -5d : %(message)s'))
log_key = 'logger_key'


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class ProgressLogFilter(logging.Filter):
    def filter(self, record):
        record.progress_id = Logger().progress_id
        return True


@singleton
class Logger(object):
    def __init__(self, progress_id='', log_file='/tmp/xxx.log'):
        self.__log_key = log_key
        self.progress_id = progress_id
        self.log_file = log_file

    def read_log(self, log_level, log_message):
        if self.progress_id == '':
            Logger().progress_id = str(uuid())
        else:
            Logger().progress_id = self.progress_id
        logger = logging.getLogger(self.__log_key)
        logger.addFilter(ProgressLogFilter())
        logger.setLevel(logging.DEBUG)

        th = logging.StreamHandler()
        th.setLevel(logging.DEBUG)

        formatter = logging.Formatter(log_fmt)
        th.setFormatter(formatter)

        logger.addHandler(th)

        level_dic = {'debug': logger.debug, 'info': logger.info, 'warning': logger.warning, 'error': logger.error,
                     'critical': logger.critical}
        level_dic[log_level](log_message)

        th.flush()
        logger.removeHandler(th)

    def write_log(self, log_level, log_message):
        if self.progress_id == '':
            Logger().progress_id = str(uuid())
        else:
            Logger().progress_id = self.progress_id
        logger = logging.getLogger(self.__log_key)
        logger.addFilter(ProgressLogFilter())
        logger.setLevel(logging.DEBUG)

        log_dir = os.path.dirname(self.log_file)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(log_fmt)
        fh.setFormatter(formatter)

        logger.addHandler(fh)

        level_dic = {'debug': logger.debug, 'info': logger.info, 'warning': logger.warning, 'error': logger.error,
                     'critical': logger.critical}
        level_dic[log_level](log_message)

        fh.flush()
        logger.removeHandler(fh)


ins_log = Logger()


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        ins_log.read_log('info', '%s execute duration :%.3f second' % (str(func), duration))
        return result

    return wrapper


