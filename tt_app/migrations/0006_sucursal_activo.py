# Generated by Django 5.0.6 on 2024-05-30 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_app', '0005_producto_disponible'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]