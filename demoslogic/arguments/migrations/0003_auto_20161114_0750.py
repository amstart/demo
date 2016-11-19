# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arguments', '0002_auto_20161114_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='aim',
            field=models.IntegerField(choices=[(1, 'The positive version of the following conclusion is true:'), (2, 'The negative version of the following conclusion is true:'), (3, 'The following is relevant:'), (4, 'The following is irrelevant:'), (5, 'To point out missing knowledge on the matter.')], default=1),
        ),
    ]