# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-25 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_auto_20170325_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='profile/2017_03_22/2__15_12_33_307511.jpg', upload_to='profile/%Y_%m_%d'),
        ),
    ]
