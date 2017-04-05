# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 11:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20170404_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fb_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='ggl_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='naver_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='guidereview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 4, 5)),
        ),
        migrations.AlterField(
            model_name='userreview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 4, 5)),
        ),
    ]
