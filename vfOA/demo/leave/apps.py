#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-10-18
# software: PyCharm


from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _


class LeaveConfig(AppConfig,ModuleMixin):
    name = 'demo.leave'
    icon = '<i class="material-icons">backup</i>'
    verbose_name = _("请假")


