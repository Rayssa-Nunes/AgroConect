# Generated by Django 5.1.5 on 2025-01-26 17:21

import core.models
import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_vendor_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, verbose_name='Nome')),
                ('image', models.ImageField(default='category.jpg', upload_to='category', verbose_name='Imagem')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Nome')),
                ('image', models.ImageField(default='product.jpg', upload_to=core.models.user_directory_path, verbose_name='Imagem')),
                ('description', models.TextField(blank=True, default='Este é um produto.', null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Preço')),
                ('old_price', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Preço antigo')),
                ('specifications', models.TextField(blank=True, null=True, verbose_name='Especificações')),
                ('type', models.CharField(blank=True, default='Orgânico', max_length=100, null=True, verbose_name='Tipo')),
                ('stock_count', models.PositiveIntegerField(default=0, verbose_name='Quantidade em estoque')),
                ('life', models.CharField(blank=True, default='100 dias', max_length=100, null=True, verbose_name='Tempo de vida')),
                ('product_status', models.CharField(choices=[('desativado', 'Desativado'), ('em_revisao', 'Em Revisão'), ('publicado', 'Publicado')], default='em_revisao', max_length=20, verbose_name='Status')),
                ('in_stock', models.BooleanField(default=True, verbose_name='Em estoque')),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=10, prefix='sku', unique=True, verbose_name='Identificador Único Atribuído')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated', models.DateTimeField(blank=True, null=True, verbose_name='Data de atualização')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.vendor')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]
