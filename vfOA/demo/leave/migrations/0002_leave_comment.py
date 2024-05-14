#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-3-9
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='comment',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='备注'),
        ),
    ]
