# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0007_auto_20161206_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='premise_type',
            field=models.IntegerField(choices=[(1, 'Categorization'), (2, 'Collection'), (3, 'Comparison'), (4, 'Relation')], default=1),
        ),
    ]
