# Generated by Django 5.1.5 on 2025-03-07 20:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_alter_fairaddress_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fair',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fairs', to='location.fairaddress'),
        ),
    ]
