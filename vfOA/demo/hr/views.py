#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-2-19
# software: PyCharm


from material.frontend.views import ModelViewSet
from . import models

class EmployeeViewSet(ModelViewSet):

    model = models.employee

class DepartmentViewSet(ModelViewSet):

    model = models.department