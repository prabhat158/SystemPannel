# Generated by Django 2.0.7 on 2018-09-01 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180812_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cr_referral_code',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
