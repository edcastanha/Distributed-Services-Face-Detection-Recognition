# Generated by Django 4.2.5 on 2023-09-20 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locais',
            old_name='ponto',
            new_name='contrato',
        ),
    ]
