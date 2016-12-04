# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-26 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0002_auto_20161126_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='premise_type',
            field=models.IntegerField(choices=[(1, 'Categorization'), (2, 'Collection'), (3, 'Comparison'), (4, 'Deduction'), (5, 'Diagnosis'), (6, 'Proposal')], default=1),
        ),
    ]
