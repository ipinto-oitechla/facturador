# Generated by Django 3.2.18 on 2023-07-25 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restser', '0009_auto_20230724_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefactura',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='fk_factura',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restser.factura'),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='monto',
            field=models.DecimalField(decimal_places=8, max_digits=11, null=True),
        ),
    ]
