#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-11-18
# software: PyCharm


from django.contrib import admin
from .models import *
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass

@admin.register(BloodTestProcess)
class BloodTestProcessAdmin(admin.ModelAdmin):
    pass