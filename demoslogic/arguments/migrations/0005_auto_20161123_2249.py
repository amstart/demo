# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arguments', '0004_auto_20161120_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='aim',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='argument',
            name='premise1_if',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='argument',
            name='premise2_if',
            field=models.IntegerField(),
        ),
    ]
