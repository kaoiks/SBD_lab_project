# Generated by Django 4.0 on 2023-01-07 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0019_alter_contractor_address_alter_driver_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_driver', to='exampleapp.address'),
        ),
    ]
