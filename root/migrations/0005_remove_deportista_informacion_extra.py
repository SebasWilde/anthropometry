# Generated by Django 2.1.4 on 2019-02-10 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0004_auto_20190210_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deportista',
            name='informacion_extra',
        ),
    ]