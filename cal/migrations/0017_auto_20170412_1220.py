# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0016_auto_20170412_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='attendees', to='accounts.Account'),
        ),
    ]
