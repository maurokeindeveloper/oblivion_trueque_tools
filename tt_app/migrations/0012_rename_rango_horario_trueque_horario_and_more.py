# Generated by Django 5.0.6 on 2024-06-05 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_app', '0011_alter_trueque_activo_alter_trueque_rango_horario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trueque',
            old_name='rango_horario',
            new_name='horario',
        ),
        migrations.AlterField(
            model_name='trueque',
            name='estado',
            field=models.IntegerField(choices=[(1, 'Solicitado'), (2, 'Pendiente'), (3, 'Aceptado'), (4, 'Concretado'), (5, 'Rechazado'), (6, 'Cancelado por empleado'), (7, 'Cancelado por solicitante'), (8, 'Cancelado por solicitado'), (9, 'Concretó otro trueque')], default=1),
        ),
        migrations.AlterField(
            model_name='trueque',
            name='fecha',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trueque',
            name='motivo_rechazo',
            field=models.IntegerField(blank=True, choices=[(1, 'Producto ya no disponible'), (2, 'Falta de interes en el producto ofrecido'), (3, 'Falta de disponibilidad en el horario solicitado'), (4, 'Falta de disponibilidad en la fecha solicitada'), (5, 'Otros motivos')], default=None, null=True),
        ),
    ]