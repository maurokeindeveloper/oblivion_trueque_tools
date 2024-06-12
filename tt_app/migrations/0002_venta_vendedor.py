# Generated by Django 5.0.6 on 2024-06-12 00:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
