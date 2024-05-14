#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-5-14
# software: PyCharm


from django.db import models
from viewflow.models import Process
from django.utils.translation import ugettext_lazy as _

class cs_process(Process):
    file=models.FileField(_('会签文件'), upload_to = './upload/')
    version = models.CharField(_('版本'), max_length=50)
    mark = models.CharField(_('备注'), max_length=1024)

    cfo_approved = models.CharField(
        max_length=1,
        choices=(
            ("1", "同意"),
            ("0", "不同意"),))

    ceo_approved = models.CharField(
        max_length=1,
        choices=(
            ("1", "同意"),
            ("0", "不同意"),))

    class Meta:
        verbose_name = _("会签")
        verbose_name_plural = _('会签')