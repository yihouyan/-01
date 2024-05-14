#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-12-1
# software: PyCharm




from functools import wraps

from flask import request

from common.common_request_process import req


def api_version(func):
    """
    API版本验证装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        xml = request.args.get('format')
        verify_result, version_res = req.verify_version(kwargs.get('version'), xml)
        if not verify_result:
            return version_res
        return func(*args, **kwargs)

    return wrapper
