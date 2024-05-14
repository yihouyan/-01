#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-11-12
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
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol_no', models.CharField(max_length=10, verbose_name='协议书编号')),
                ('task_no', models.CharField(max_length=10, verbose_name='任务流水号')),
                ('product_type', models.CharField(max_length=1024, verbose_name='产品名称/规格型号')),
                ('product_num', models.IntegerField(verbose_name='数量')),
                ('sample_from', models.CharField(max_length=1, verbose_name='来样方式')),
                ('sample_to', models.CharField(max_length=1, verbose_name='样品处理')),
                ('report_get', models.CharField(max_length=1, verbose_name='报告领取')),
                ('testing_area', models.CharField(max_length=1, verbose_name='测试地点')),
                ('report_num', models.IntegerField(help_text='份数', verbose_name='报告份数')),
                ('testing_class', models.CharField(max_length=1, verbose_name='检测类别')),
                ('testing_time_class', models.CharField(max_length=1, verbose_name='检测时间')),
                ('testing_time', models.IntegerField(blank=True, help_text='工作日', null=True, verbose_name='加急')),
                ('testing_fee', models.FloatField(help_text='元', verbose_name='测试费用')),
                ('testing_fee_tax_no', models.CharField(max_length=1024, verbose_name='发票号')),
                ('testing_fee_tax_class', models.CharField(max_length=1, verbose_name='发票类别')),
                ('testing_status', models.CharField(max_length=1, verbose_name='检测状态')),
                ('create_datetime', models.DateTimeField(verbose_name='创建日期')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '协议书',
                'verbose_name_plural': '协议书',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='单位名称')),
                ('address', models.CharField(max_length=1024, verbose_name='单位地址')),
                ('telephone', models.CharField(max_length=1024, verbose_name='电话')),
                ('atten', models.CharField(max_length=1024, verbose_name='联系人')),
                ('postcode', models.CharField(max_length=1024, verbose_name='邮编')),
                ('fax', models.CharField(max_length=1024, verbose_name='传真')),
            ],
            options={
                'verbose_name': '委托单位',
                'verbose_name_plural': '委托单位',
            },
        ),
        migrations.CreateModel(
            name='TestingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='测试项名称')),
            ],
            options={
                'verbose_name': '测试项目',
                'verbose_name_plural': '测试项目',
            },
        ),
        migrations.CreateModel(
            name='TestingItemTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='模板名称')),
                ('items', models.ManyToManyField(to='testing.TestingItem', verbose_name='测试项目')),
            ],
            options={
                'verbose_name': '测试项目模板',
                'verbose_name_plural': '测试项目模板',
            },
        ),
        migrations.CreateModel(
            name='TestingStandard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='标准名称')),
                ('no', models.CharField(max_length=10, verbose_name='协议号')),
                ('st_class', models.CharField(choices=[('0', '国标'), ('1', '行标'), ('2', '企标')], max_length=1, verbose_name='标准类别')),
            ],
            options={
                'verbose_name': '标准',
                'verbose_name_plural': '标准',
            },
        ),
        migrations.CreateModel(
            name='TestingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='测试类型')),
                ('mark', models.CharField(max_length=1024, verbose_name='备注')),
            ],
        ),
        migrations.AddField(
            model_name='testingitem',
            name='testing_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.TestingType', verbose_name='标准类别'),
        ),
        migrations.AddField(
            model_name='contract',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='testing.Customer', verbose_name='委托单位'),
        ),
        migrations.AddField(
            model_name='contract',
            name='testing_items',
            field=models.ManyToManyField(to='testing.TestingItem', verbose_name='测试项目'),
        ),
        migrations.AddField(
            model_name='contract',
            name='testing_standards',
            field=models.ManyToManyField(to='testing.TestingStandard', verbose_name='检测依据'),
        ),
        migrations.AddField(
            model_name='contract',
            name='testing_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.TestingType', verbose_name='标准类别'),
        ),
    ]
