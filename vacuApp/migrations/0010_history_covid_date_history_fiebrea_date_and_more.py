# Generated by Django 4.0.4 on 2022-05-18 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacuApp', '0009_remove_history_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='covid_date',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='fiebreA_date',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='gripe_date',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
    ]
