# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-02 08:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20160928_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='premise',
            old_name='text',
            new_name='subject',
        ),
    ]
