# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0026_auto_20170326_0203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accomtemplate',
            name='pic_list',
        ),
        migrations.RemoveField(
            model_name='guidetemplate',
            name='picture',
        ),
        migrations.AddField(
            model_name='accomtemplate',
            name='photo',
            field=models.FileField(default='', upload_to='accom_photos/%Y_%m_%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guidetemplate',
            name='photo',
            field=models.FileField(default='', upload_to='guide_photos/%Y_%m_%d'),
            preserve_default=False,
        ),
    ]
