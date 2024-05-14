#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-11-15
# software: PyCharm


from django.contrib import admin
from .models import *
@admin.register(cs_process)
class CSAdmin(admin.ModelAdmin):
    list_display = ( 'version', 'mark')