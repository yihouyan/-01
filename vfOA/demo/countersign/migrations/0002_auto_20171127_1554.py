#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-4-10
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countersign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cs_process',
            name='file',
            field=models.FileField(default='blank', upload_to='./upload/', verbose_name='会签文件'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cs_process',
            name='ceo_approved',
            field=models.CharField(choices=[('1', '同意'), ('0', '不同意')], max_length=1),
        ),
        migrations.AlterField(
            model_name='cs_process',
            name='cfo_approved',
            field=models.CharField(choices=[('1', '同意'), ('0', '不同意')], max_length=1),
        ),
    ]
