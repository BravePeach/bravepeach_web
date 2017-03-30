# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 05:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_auto_20170329_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accomtemplate',
            name='photo',
            field=django_mysql.models.ListTextField(models.CharField(max_length=100), size=None),
        ),
        migrations.AlterField(
            model_name='guidereview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 3, 30)),
        ),
        migrations.AlterField(
            model_name='userreview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 3, 30)),
        ),
    ]
