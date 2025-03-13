# Generated by Django 5.1.5 on 2025-03-11 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0007_alter_fairday_unique_together_fairday_fair_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fair',
            name='address',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fairs', to='location.fairaddress'),
        ),
    ]
