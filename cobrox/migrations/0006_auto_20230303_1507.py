# Generated by Django 3.2.18 on 2023-03-03 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0005_auto_20230302_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='celular',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='credito',
            name='estadocredito',
            field=models.PositiveIntegerField(choices=[(0, 'VIGENTE'), (2, 'CANCELADO')], help_text='Seleccione el Estado del Crédito'),
        ),
    ]
