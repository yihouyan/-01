#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2022-6-16
# software: PyCharm


from django.contrib import admin

from django.contrib import admin
from .models import *
@admin.register(department)
class departmentAdmin(admin.ModelAdmin):
    pass

@admin.register(employee)
class employeeAdmin(admin.ModelAdmin):
    pass