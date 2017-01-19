# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-17 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtweet', '0011_auto_20170116_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(related_name='followers', to='mtweet.UserProfile'),
        ),
    ]
