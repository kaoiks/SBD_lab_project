# Generated by Django 4.0 on 2023-01-07 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0025_alter_route_contractor_alter_route_driver_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('saturdays', models.IntegerField()),
                ('days_stationary', models.IntegerField()),
                ('days_leave', models.IntegerField()),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='driver_settlement', to='exampleapp.driver')),
            ],
        ),
    ]
