# Generated by Django 3.2.18 on 2023-03-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobrox', '0018_auto_20230316_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='historicalcliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
