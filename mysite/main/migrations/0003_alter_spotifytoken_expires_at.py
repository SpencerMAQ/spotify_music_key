# Generated by Django 4.1.1 on 2022-09-13 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_spotifytoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifytoken',
            name='expires_at',
            field=models.FloatField(),
        ),
    ]
