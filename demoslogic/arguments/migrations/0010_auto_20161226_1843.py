# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-26 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arguments', '0009_auto_20161226_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='premise2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='premise2', to='premises.Premise'),
        ),
        migrations.AlterField(
            model_name='argument',
            name='premise3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='premise3', to='premises.Premise'),
        ),
    ]
