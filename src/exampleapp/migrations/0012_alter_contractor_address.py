# Generated by Django 4.0 on 2022-12-26 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0011_remove_contractor_id_alter_contractor_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='exampleapp.address'),
        ),
    ]
