# Generated by Django 5.0.6 on 2024-06-05 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_app', '0013_rename_fecha_trueque_fecha_de_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trueque',
            name='fecha_de_solicitud',
            field=models.DateField(auto_now=True),
        ),
    ]
