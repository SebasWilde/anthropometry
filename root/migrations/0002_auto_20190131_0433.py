# Generated by Django 2.1.4 on 2019-01-31 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institucion',
            old_name='foto',
            new_name='logo',
        ),
    ]
