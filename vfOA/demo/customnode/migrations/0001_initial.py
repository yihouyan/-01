#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-10-27
# software: PyCharm


from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewflow', '0006_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DynamicSplitProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('question', models.CharField(max_length=50)),
                ('split_count', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.AddField(
            model_name='decision',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customnode.DynamicSplitProcess'),
        ),
        migrations.AddField(
            model_name='decision',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
