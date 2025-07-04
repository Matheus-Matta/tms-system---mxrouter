# Generated by Django 5.2 on 2025-05-26 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmsapp', '0011_alter_delivery_latitude_alter_delivery_longitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='total_volume_m3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Capacidade (m³)'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='total_weight_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Capacidade (kg)'),
        ),
        migrations.AlterField(
            model_name='historicaldelivery',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='historicaldelivery',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='historicaldelivery',
            name='total_volume_m3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Capacidade (m³)'),
        ),
        migrations.AlterField(
            model_name='historicaldelivery',
            name='total_weight_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Capacidade (kg)'),
        ),
    ]
