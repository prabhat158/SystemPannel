# Generated by Django 2.0.7 on 2018-12-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proshows', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proshowsevent',
            name='image',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='proshowsevent',
            name='link',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
