# Generated by Django 5.1.5 on 2025-01-25 21:16

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128, verbose_name='Logradouro')),
                ('district', models.CharField(max_length=128, verbose_name='Bairro')),
                ('number', models.CharField(blank=True, max_length=128, null=True, verbose_name='Número')),
                ('city', models.CharField(max_length=128, verbose_name='Cidade')),
                ('state', models.CharField(max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=8, verbose_name='CEP')),
                ('status', models.BooleanField(default=False, verbose_name='Endereço padrão?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='vendor.jpg', upload_to=core.models.user_directory_path, verbose_name='Imagem de perfil')),
                ('cover_image', models.ImageField(default='vendor.jpg', upload_to=core.models.user_directory_path, verbose_name='Imagem de capa')),
                ('description', models.TextField(blank=True, default='Eu amo ser um vendedor de produtos naturais.', null=True, verbose_name='Descrição')),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True, verbose_name='CNPJ')),
                ('legal_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Razão social')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
            },
        ),
    ]
