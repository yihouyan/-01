#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-6-15
# software: PyCharm


from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from material.frontend.registry import modules


class HrConfig(AppConfig,ModuleMixin):
    name = 'demo.hr'
    label = 'hr'
    verbose_name='资源管理'
    icon = '<i class="material-icons">book</i>'
