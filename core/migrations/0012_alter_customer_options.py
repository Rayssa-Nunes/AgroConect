# Generated by Django 5.1.5 on 2025-03-11 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('view_customer_dashboard', 'Can view customer dashboard'), ('edit_cusotmer_profile', 'Can edit customer profile')], 'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
    ]
