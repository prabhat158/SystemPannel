# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-07 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionsEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('rules', models.TextField()),
                ('prizes', models.TextField()),
                ('minparticipants', models.TextField(default=0)),
                ('maxparticipants', models.TextField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionsGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='competitionsevent',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='competitions.CompetitionsGenre'),
        ),
    ]