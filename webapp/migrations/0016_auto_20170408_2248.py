# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 13:48
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0015_merge_20170406_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideAlarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=200)),
                ('landing', models.CharField(max_length=100, null=True)),
                ('immediate', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='webapp.Guide')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAlarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(max_length=200)),
                ('landing', models.CharField(max_length=100, null=True)),
                ('immediate', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Guide')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='guidereview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 4, 8)),
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='landmark',
            field=models.CharField(blank=True, default='없음', max_length=200),
        ),
        migrations.AlterField(
            model_name='userreview',
            name='write_date',
            field=models.DateField(default=datetime.date(2017, 4, 8)),
        ),
    ]
