#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-1-9
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viewflow', '0006_i18n'),
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_date', models.DateTimeField(verbose_name='申请时间')),
                ('position', models.CharField(max_length=256, verbose_name='职位')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='结束时间')),
                ('resion', models.CharField(max_length=256, verbose_name='请假事由')),
                ('file_url', models.CharField(max_length=256, verbose_name='上传附件')),
                ('depart_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.department', verbose_name='部门')),
                ('req_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee', verbose_name='申请人')),
            ],
            options={
                'verbose_name': '请假',
                'verbose_name_plural': '请假',
                'db_table': 'leave',
            },
        ),
        migrations.CreateModel(
            name='Leave_class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
            ],
            options={
                'verbose_name': '请假类别',
                'verbose_name_plural': '请假类别',
                'db_table': 'leave_class',
            },
        ),
        migrations.CreateModel(
            name='LeaveProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('dep_approved', models.BooleanField(default=False, verbose_name='部门审核')),
                ('dep_approved_time', models.DateTimeField(blank=True, null=True, verbose_name='部门领导审核时间')),
                ('dep_approved_comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='部门领导审核意见')),
                ('hr_approved', models.BooleanField(default=False, verbose_name='人事审核')),
                ('hr_approved_time', models.DateTimeField(blank=True, null=True, verbose_name='人事审核时间')),
                ('hr_approved_comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='人事审核意见')),
                ('comment', models.CharField(blank=True, max_length=1024, null=True)),
                ('leave', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leave.Leave')),
            ],
            options={
                'verbose_name': '请假过程',
                'verbose_name_plural': '请假过程',
                'db_table': 'leave_process',
            },
            bases=('viewflow.process',),
        ),
        migrations.AddField(
            model_name='leave',
            name='req_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Leave_class', verbose_name='请假类别'),
        ),
    ]
