# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 09:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arguments', '0004_auto_20161107_0653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='argumentvote',
            name='staged',
        ),
    ]
