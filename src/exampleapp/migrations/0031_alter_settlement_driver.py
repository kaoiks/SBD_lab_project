# Generated by Django 4.0 on 2023-01-07 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0030_settlement_rate_for_kilometer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settlement',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='settlements', to='exampleapp.driver'),
        ),
    ]
