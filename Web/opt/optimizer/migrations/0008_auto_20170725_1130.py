# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optimizer', '0007_auto_20170725_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='optimizer.Time'),
        ),
    ]
