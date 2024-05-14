#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-11-27
# software: PyCharm


from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(
        url='./departments/'), name="index"),
    url('^departments/', include(views.DepartmentViewSet().urls)),
    url('^employees/', include(views.EmployeeViewSet().urls)),
]
