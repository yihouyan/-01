#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-6-21
# software: PyCharm



import shortuuid
from websdk.base_handler import BaseHandler as SDKBaseHandler


class BaseHandler(SDKBaseHandler):
    def __init__(self, *args, **kwargs):
        self.new_csrf_key = str(shortuuid.uuid())
        super(BaseHandler, self).__init__(*args, **kwargs)

