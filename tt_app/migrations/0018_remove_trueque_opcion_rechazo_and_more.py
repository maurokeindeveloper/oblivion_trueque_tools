# Generated by Django 5.0.6 on 2024-06-05 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_app', '0017_merge_20240605_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trueque',
            name='opcion_rechazo',
        ),
        migrations.AlterField(
            model_name='trueque',
            name='motivo_rechazo',
            field=models.IntegerField(blank=True, choices=[(1, 'Producto ya no disponible'), (2, 'Falta de interés en el producto ofrecido'), (3, 'Falta de disponibilidad en el horario solicitado'), (4, 'Falta de disponibilidad en la fecha solicitada'), (5, 'Otros motivos')], default=None, null=True),
        ),
    ]