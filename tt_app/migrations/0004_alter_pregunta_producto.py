# Generated by Django 5.0.4 on 2024-05-29 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_app', '0003_merge_20240529_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregunta',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='tt_app.producto'),
        ),
    ]
