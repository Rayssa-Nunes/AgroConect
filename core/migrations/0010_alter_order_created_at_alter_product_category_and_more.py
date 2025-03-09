# Generated by Django 5.1.5 on 2025-03-04 20:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_date_created_order_created_at_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='Este é um produto.', null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='product',
            name='life',
            field=models.CharField(blank=True, default='100 dias', max_length=100, null=True, verbose_name='Vida útil'),
        ),
    ]
