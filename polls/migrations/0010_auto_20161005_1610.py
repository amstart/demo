# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-05 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20161004_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='object',
            field=models.CharField(default='', max_length=200),
        ),
    ]
