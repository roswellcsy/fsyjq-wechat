# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-28 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20180128_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_city',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_country',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='国家'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_province',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='省份'),
        ),
    ]
