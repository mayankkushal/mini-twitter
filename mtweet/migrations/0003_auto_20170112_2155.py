# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-12 16:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mtweet', '0002_auto_20170112_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='home_town',
            new_name='hometown',
        ),
    ]
