# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2019-08-11 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fplcornerapp', '0002_auto_20190803_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Fpldata',
        ),
    ]
