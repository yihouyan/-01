#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-1-17
# software: PyCharm


from django.conf.urls import url, include
from django.views import generic
from . import views

urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./employee/', permanent=False), name="index"),
    url('^employee/', include(views.EmployeeViewSet().urls)),
    url('^department/', include(views.DepartmentViewSet().urls)),
]