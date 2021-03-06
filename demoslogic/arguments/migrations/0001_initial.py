# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 17:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('premises', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('staged', models.DateTimeField(blank=True, null=True)),
                ('aim', models.IntegerField(choices=[(1, 'To support the positive version of the conclusion.'), (2, 'To support the negative version of the conclusion.'), (3, 'To point why a decision on the matter is required soon.'), (4, 'To point out missing knowledge on the matter.')], default=1)),
                ('conclusion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conclusion', to='premises.Premise')),
                ('premise1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='premise1', to='premises.Premise')),
                ('premise2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='premise2', to='premises.Premise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'pub_date',
            },
        ),
        migrations.CreateModel(
            name='ArgumentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('last_voted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last voted')),
                ('value', models.IntegerField(choices=[(1, 'completely invalid'), (2, 'weak'), (3, 'strong'), (4, 'completely valid')], default=1)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arguments.Argument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
