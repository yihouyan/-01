#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-11-9
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0002_i18n'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sea',
            name='area',
            field=models.BigIntegerField(help_text='平方公里', verbose_name='area'),
        ),
    ]
