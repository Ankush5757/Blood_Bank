# Generated by Django 5.1 on 2024-12-05 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donate_Us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_id', models.CharField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.register')),
            ],
        ),
    ]
