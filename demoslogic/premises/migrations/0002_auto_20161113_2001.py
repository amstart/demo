# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('premises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='premise',
            name='key_predicate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='premises.Verb'),
        ),
    ]
