# Generated by Django 4.0 on 2022-12-26 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0008_address_city_address_type_contractor_address_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('street', 'postal_code', 'city')},
        ),
    ]
