# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_auto_20170408_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidealarm',
            name='landing',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]