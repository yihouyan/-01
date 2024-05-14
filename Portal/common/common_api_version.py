#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-2-23
# software: PyCharm



from enum import Enum, unique


@unique
class apiVersion(Enum):
    """
    api 版本枚举
    """
    version1 = 'v1'
    version2 = 'v2'
