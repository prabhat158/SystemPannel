# Generated by Django 2.0.7 on 2019-09-25 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livewire', '0005_auto_20190925_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livewireband',
            name='emailid',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='livewireband',
            name='original_composition',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
