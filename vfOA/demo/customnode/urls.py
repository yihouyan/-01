#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2022-3-21
# software: PyCharm


from viewflow.flow.viewset import FlowViewSet
from .flows import DynamicSplitFlow


urlpatterns = FlowViewSet(DynamicSplitFlow).urls
