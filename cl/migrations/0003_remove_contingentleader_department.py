# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-05 09:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cl', '0002_auto_20171004_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contingentleader',
            name='department',
        ),
    ]
