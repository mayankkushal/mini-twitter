# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-13 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtweet', '0006_auto_20170112_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timeposted',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='timeposted',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='display_picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
