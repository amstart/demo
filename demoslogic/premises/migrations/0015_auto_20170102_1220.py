# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-02 11:20
from __future__ import unicode_literals

import demoslogic.premises.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('premises', '0014_premisevote_value2'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjective',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AddField(
            model_name='adjective',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noun',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AddField(
            model_name='noun',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verb',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AddField(
            model_name='verb',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adjective',
            name='name',
            field=demoslogic.premises.models.TrimmedCharField(default='', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='premise',
            name='premise_type',
            field=models.IntegerField(choices=[(1, 'Categorization'), (2, 'Collection'), (3, 'Comparison'), (4, 'Correlation'), (5, 'Existence'), (6, 'Encouragment')], default=1),
        ),
    ]
