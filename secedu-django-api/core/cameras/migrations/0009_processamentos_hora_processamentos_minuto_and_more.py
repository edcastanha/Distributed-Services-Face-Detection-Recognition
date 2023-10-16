# Generated by Django 4.2.5 on 2023-10-16 16:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0008_processamentos_dia_alter_processamentos_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='processamentos',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now, unique_for_date='dia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processamentos',
            name='minuto',
            field=models.TimeField(default=django.utils.timezone.now, unique_for_date='hora'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='processamentos',
            name='dia',
            field=models.DateField(unique=True),
        ),
    ]
