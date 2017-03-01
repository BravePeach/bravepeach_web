# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 04:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20170227_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccomTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('map', models.CharField(max_length=200)),
                ('guide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Guide')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=100)),
                ('offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.GuideOffer')),
            ],
        ),
        migrations.CreateModel(
            name='GuideTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('picture', models.CharField(max_length=200)),
                ('guide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Guide')),
            ],
        ),
    ]