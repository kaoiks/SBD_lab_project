# Generated by Django 4.0 on 2022-12-26 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exampleapp', '0007_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='a', max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='type',
            field=models.CharField(choices=[(1, 'Contractor'), (2, 'Driver')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contractor',
            name='address',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='exampleapp.address'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='name',
            field=models.CharField(default='ESSA', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='route',
            name='distance',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('contractor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='exampleapp.contractor')),
            ],
        ),
    ]