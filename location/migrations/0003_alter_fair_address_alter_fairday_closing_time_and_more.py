# Generated by Django 5.1.5 on 2025-03-07 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_fairaddress_options_remove_fair_days_fairday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fair',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.fairaddress'),
        ),
        migrations.AlterField(
            model_name='fairday',
            name='closing_time',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AlterField(
            model_name='fairday',
            name='day',
            field=models.CharField(choices=[('seg', 'Segunda-feira'), ('ter', 'Terça-feira'), ('qua', 'Quarta-feira'), ('qui', 'Quinta-feira'), ('sex', 'Sexta-feira'), ('sab', 'Sábado'), ('dom', 'Domingo')], max_length=30),
        ),
        migrations.AlterField(
            model_name='fairday',
            name='opening_time',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
