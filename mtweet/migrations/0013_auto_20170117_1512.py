# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-17 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtweet', '0012_userprofile_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followers', to='mtweet.UserProfile'),
        ),
    ]
