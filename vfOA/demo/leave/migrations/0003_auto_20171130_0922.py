#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-11-23
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_leave_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveprocess',
            name='dep_approved',
            field=models.IntegerField(default=0, verbose_name='部门审核'),
        ),
        migrations.AlterField(
            model_name='leaveprocess',
            name='hr_approved',
            field=models.IntegerField(default=0, verbose_name='人事审核'),
        ),
    ]
