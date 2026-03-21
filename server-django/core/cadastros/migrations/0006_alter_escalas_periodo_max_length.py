# Generated migration for Escalas.periodo max_length increase

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_alter_fotos_pessoa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escalas',
            name='periodo',
            field=models.CharField(
                choices=[
                    ('Entrada', 'Entrada'),
                    ('Período 1', 'Período 1'),
                    ('Período 2', 'Período 2'),
                    ('Período 3', 'Período 3'),
                    ('Período 4', 'Período 4'),
                    ('Período 5', 'Período 5'),
                    ('Período 6', 'Período 6'),
                    ('Período 7', 'Período 7'),
                    ('Período 8', 'Período 8'),
                    ('Período 9', 'Período 9'),
                    ('Extra', 'Extra'),
                    ('Intervalo', 'Intervalo'),
                    ('Saida', 'Saida'),
                ],
                default='Entrada',
                max_length=15,
            ),
        ),
    ]
