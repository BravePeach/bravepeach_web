# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_auto_20170322_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to='profile/%Y_%m_%d'),
        ),
    ]