#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-3-16
# software: PyCharm


from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Department Name')),
                ('note', models.CharField(max_length=1024, verbose_name='Note')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'db_table': 'hr.department',
            },
        ),
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateTimeField(verbose_name='Date of Birth')),
                ('passport_id', models.CharField(max_length=1024, verbose_name='passport No')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('marital', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], max_length=10)),
                ('address', models.CharField(max_length=1024, verbose_name='Working Address')),
                ('work_phone', models.CharField(max_length=1024, verbose_name='Work Phone')),
                ('mobile_phone', models.CharField(max_length=1024, verbose_name='Work Mobile')),
                ('work_email', models.CharField(max_length=1024, verbose_name='Work Email')),
                ('work_location', models.CharField(max_length=1024, verbose_name='Office Location')),
                ('notes', models.CharField(max_length=1024, verbose_name='Notes')),
                ('Manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_member', to='hr.employee')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='hr.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='账号绑定')),
            ],
            options={
                'verbose_name': '雇员',
                'verbose_name_plural': '雇员',
                'db_table': 'hr.employee',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_children', to='hr.employee'),
        ),
        migrations.AddField(
            model_name='department',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dep_children', to='hr.department'),
        ),
    ]
