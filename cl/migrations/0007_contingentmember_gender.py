# Generated by Django 2.0.7 on 2018-10-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cl', '0006_contingent_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='contingentmember',
            name='gender',
            field=models.CharField(default=None, max_length=6),
        ),
    ]