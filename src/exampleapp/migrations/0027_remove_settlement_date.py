# Generated by Django 4.0 on 2023-01-07 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0026_settlement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settlement',
            name='date',
        ),
    ]
