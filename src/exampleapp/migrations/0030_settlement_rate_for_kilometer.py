# Generated by Django 4.0 on 2023-01-07 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0029_alter_settlement_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='settlement',
            name='rate_for_kilometer',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]