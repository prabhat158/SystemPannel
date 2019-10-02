# Generated by Django 2.0.7 on 2019-09-24 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livewire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='livewireband',
            name='city',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='livewireband',
            name='preferred_city',
            field=models.CharField(blank=True, choices=[('pune', 'pune'), ('bangalore', 'bangalore'), ('delhi', 'delhi'), ('shillong', 'shillong'), ('mumbai', 'mumbai')], max_length=10),
        ),
    ]
