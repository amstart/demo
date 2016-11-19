# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arguments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='argument',
            name='premise1_if_clauses',
            field=models.IntegerField(choices=[(1, 'If the positive version of the following statement is given:'), (2, 'If the negative version of the following statement is given:'), (3, 'If the following affects most people:'), (4, 'If there is missing knowledge on the following matter:')], default=1),
        ),
        migrations.AddField(
            model_name='argument',
            name='premise2_if_clauses',
            field=models.IntegerField(choices=[(1, 'If the positive version of the following statement is given:'), (2, 'If the negative version of the following statement is given:'), (3, 'If the following affects most people:'), (4, 'If there is missing knowledge on the following matter:')], default=1),
        ),
        migrations.AlterField(
            model_name='argument',
            name='aim',
            field=models.IntegerField(choices=[(1, 'To support the positive version of the conclusion.'), (2, 'To support the negative version of the conclusion.'), (3, 'To point out why the conclusion treats a problem which affects most people.'), (4, 'To point out missing knowledge on the matter.')], default=1),
        ),
    ]