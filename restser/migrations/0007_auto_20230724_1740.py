# Generated by Django 3.2.18 on 2023-07-24 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restser', '0006_auto_20230724_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='fk_detalle',
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='fk_factura',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restser.factura'),
        ),
    ]