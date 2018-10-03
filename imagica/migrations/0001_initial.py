# Generated by Django 2.0.7 on 2018-09-23 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('mobile_number', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=300)),
                ('ticketPrice', models.IntegerField()),
                ('ticketName', models.CharField(max_length=500)),
                ('college', models.CharField(max_length=500)),
                ('cr_referral_code', models.CharField(blank=True, max_length=8)),
                ('bus_pickup', models.CharField(max_length=35)),
            ],
        ),
    ]
