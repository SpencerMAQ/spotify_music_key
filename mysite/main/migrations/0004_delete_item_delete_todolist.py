# Generated by Django 4.1.1 on 2022-09-13 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_spotifytoken_expires_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='ToDoList',
        ),
    ]