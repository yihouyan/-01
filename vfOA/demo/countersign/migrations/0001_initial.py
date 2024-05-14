#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-12-26
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viewflow', '0006_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='cs_process',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('version', models.CharField(max_length=50, verbose_name='版本')),
                ('mark', models.CharField(max_length=1024, verbose_name='备注')),
                ('cfo_approved', models.CharField(choices=[('1', '同意'), ('2', '不同意')], max_length=1)),
                ('ceo_approved', models.CharField(choices=[('1', '同意'), ('2', '不同意')], max_length=1)),
            ],
            options={
                'verbose_name': '会签',
                'verbose_name_plural': '会签',
            },
            bases=('viewflow.process',),
        ),
    ]
