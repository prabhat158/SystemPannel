# Generated by Django 2.0.7 on 2018-10-28 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cl', '0012_visits'),
    ]

    operations = [
        migrations.AddField(
            model_name='visits',
            name='gender',
            field=models.CharField(default=None, max_length=6),
        ),
    ]
