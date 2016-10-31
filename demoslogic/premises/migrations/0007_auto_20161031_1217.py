# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0006_auto_20161027_2141'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Argument',
        ),
        migrations.AlterModelOptions(
            name='premise',
            options={'get_latest_by': 'pub_date'},
        ),
        migrations.AlterField(
            model_name='categorizationvote',
            name='value',
            field=models.IntegerField(choices=[(1, 'Not accurate at all or very little'), (2, 'Barely useful'), (3, 'Useful'), (4, 'Completely accurate')], default=1),
        ),
    ]
