#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-10-24
# software: PyCharm




import logging
import os
import logging.handlers

lg = logging.getLogger("Error")


def init_log():
    log_path = os.getcwd() + "/var/log"
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    except:
        print("创建日志目录失败")
        exit(1)
    if len(lg.handlers) == 0:  # 避免重复
        filename = os.path.join(log_path, 'user_api.log')
        fh = logging.FileHandler(filename, mode="a", encoding="utf-8")  # 默认mode 为a模式，默认编码方式为utf-8
        sh = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - Model:%(filename)s - Fun:%(funcName)s - Message:%(message)s - Line:%(lineno)d')
        lg.addHandler(fh)
        lg.addHandler(sh)
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        lg.setLevel(40)
        fh.setLevel(40)
        sh.setLevel(40)
