# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 16:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0026_auto_20170411_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidereview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 4, 13)),
        ),
        migrations.AlterField(
            model_name='userreview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 4, 13)),
        ),
    ]
