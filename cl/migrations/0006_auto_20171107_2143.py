# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-07 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cl', '0005_auto_20171030_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contingent',
            name='cl',
        ),
        migrations.RemoveField(
            model_name='contingent',
            name='contigent_city',
        ),
        migrations.RemoveField(
            model_name='contingent',
            name='contingent_college',
        ),
        migrations.RemoveField(
            model_name='contingent',
            name='contingent_members',
        ),
        migrations.DeleteModel(
            name='Contingent',
        ),
    ]
