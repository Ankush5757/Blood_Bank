# Generated by Django 5.1.3 on 2024-12-07 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_alter_request_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='request',
            name='updated_at',
        ),
    ]
