# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_auto_20160910_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
