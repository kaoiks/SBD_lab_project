# Generated by Django 4.0 on 2022-12-26 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0016_alter_invoice_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='country_id',
            field=models.CharField(max_length=2),
        ),
    ]
