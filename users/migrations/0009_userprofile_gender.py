# Generated by Django 2.0.7 on 2018-09-23 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180918_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default='NULL', max_length=7),
        ),
    ]
