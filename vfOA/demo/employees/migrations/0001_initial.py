#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-10-23
# software: PyCharm


from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_no', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=40, unique=True)),
            ],
            options={
                'ordering': ['dept_no'],
                'db_table': 'departments',
            },
        ),
        migrations.CreateModel(
            name='DeptEmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('department', models.ForeignKey(db_column='dept_no', on_delete=django.db.models.deletion.DO_NOTHING, to='employees.Department')),
            ],
            options={
                'db_table': 'dept_emp',
            },
        ),
        migrations.CreateModel(
            name='DeptManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('department', models.ForeignKey(db_column='dept_no', on_delete=django.db.models.deletion.DO_NOTHING, to='employees.Department')),
            ],
            options={
                'ordering': ['-from_date'],
                'db_table': 'dept_manager',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('emp_no', models.IntegerField(primary_key=True, serialize=False)),
                ('birth_date', models.DateField()),
                ('first_name', models.CharField(max_length=14)),
                ('last_name', models.CharField(max_length=16)),
                ('gender', models.CharField(max_length=1)),
                ('hire_date', models.DateField()),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('employee', models.ForeignKey(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, to='employees.Employee')),
            ],
            options={
                'verbose_name': 'Salary',
                'verbose_name_plural': 'Salaries',
                'ordering': ['-from_date'],
                'db_table': 'salaries',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, to='employees.Employee')),
            ],
            options={
                'db_table': 'titles',
            },
        ),
        migrations.AddField(
            model_name='deptmanager',
            name='employee',
            field=models.ForeignKey(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='deptemp',
            name='employee',
            field=models.ForeignKey(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, to='employees.Employee'),
        ),
    ]
