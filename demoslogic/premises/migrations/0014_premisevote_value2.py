# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-30 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0013_auto_20161230_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='premisevote',
            name='value2',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
