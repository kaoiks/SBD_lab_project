# Generated by Django 4.0 on 2022-12-23 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0004_alter_cost_invoice_id_alter_cost_repair_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='invoice_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
