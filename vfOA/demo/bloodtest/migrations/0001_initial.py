#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-11-9
# software: PyCharm


from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewflow', '0006_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='Biochemistry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hemoglobin', models.IntegerField(help_text='g/dL')),
                ('lymphocytes', models.DecimalField(decimal_places=1, help_text='10^9/L', max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='BloodSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taken_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BloodTestProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodtest.BloodSample')),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='Hormones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acth', models.DecimalField(decimal_places=1, help_text='pmol/L', max_digits=3)),
                ('estradiol', models.IntegerField(help_text='ng/dL')),
                ('free_t3', models.DecimalField(decimal_places=1, help_text='ng/dL', max_digits=3)),
                ('free_t4', models.IntegerField(help_text='pmol/L')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bloodtest.BloodSample')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=250)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('U', 'Unknown')], max_length=1)),
                ('weight', models.DecimalField(decimal_places=1, help_text='kg', max_digits=4)),
                ('height', models.IntegerField(help_text='cm')),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TumorMarkers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alpha_fetoprotein', models.IntegerField(help_text='ng/mL')),
                ('beta_gonadotropin', models.IntegerField(help_text='IU/I')),
                ('ca19', models.IntegerField(help_text='U/mL')),
                ('cea', models.IntegerField(help_text='ug/L')),
                ('pap', models.IntegerField(help_text='U/dL')),
                ('pas', models.IntegerField(help_text='ug/L')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bloodtest.BloodSample')),
            ],
        ),
        migrations.AddField(
            model_name='bloodsample',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloodtest.Patient'),
        ),
        migrations.AddField(
            model_name='bloodsample',
            name='taken_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='biochemistry',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bloodtest.BloodSample'),
        ),
    ]
