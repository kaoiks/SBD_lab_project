# Generated by Django 4.0 on 2023-01-07 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0027_remove_settlement_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settlement',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='driver_settlement', to='exampleapp.driver'),
        ),
    ]
