# Generated by Django 5.1.4 on 2024-12-09 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('currency_pair', models.CharField(blank=True, max_length=7, null=True)),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_exchange_rate', to='currency.currency')),
                ('target_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_exchange_rate', to='currency.currency')),
            ],
        ),
    ]
