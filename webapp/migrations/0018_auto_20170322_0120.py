# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 16:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0017_merge_20170321_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('content', redactor.fields.RedactorField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_review', to='webapp.GuideOffer')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Guide')),
            ],
        ),
        migrations.CreateModel(
            name='UserLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Guide')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('content', redactor.fields.RedactorField()),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to='webapp.GuideOffer')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Guide')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Like',
            new_name='GuideLike',
        ),
        migrations.RemoveField(
            model_name='review',
            name='guide',
        ),
        migrations.RemoveField(
            model_name='review',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.RemoveField(
            model_name='guidelike',
            name='user',
        ),
        migrations.AddField(
            model_name='guidelike',
            name='request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webapp.UserRequest'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
