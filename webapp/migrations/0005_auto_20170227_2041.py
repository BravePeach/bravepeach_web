# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 11:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0004_accomtemplate_cost_guidetemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_num', models.CharField(max_length=11, null=True)),
                ('is_guide', models.BooleanField(default=False)),
                ('delete_reason', models.IntegerField(null=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('nationality', models.CharField(max_length=40, null=True)),
                ('birthday', models.DateField()),
                ('gender', models.BooleanField()),
                ('profile_image', models.URLField(default='')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('delete_reason_optional', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='delete_reason',
        ),
        migrations.RemoveField(
            model_name='user',
            name='delete_reason_optional',
        ),
        migrations.RemoveField(
            model_name='user',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_guide',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_num',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pw',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rating',
        ),
        migrations.AddField(
            model_name='userrequest',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guide',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guideoffer',
            name='guide_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webapp.User'),
        ),
    ]
