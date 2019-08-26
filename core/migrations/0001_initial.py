# Generated by Django 2.2.2 on 2019-08-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pessoa', models.CharField(max_length=20)),
                ('nome', models.CharField(max_length=200)),
                ('sexo', models.CharField(max_length=20)),
                ('cpf_cnpj', models.CharField(max_length=14)),
                ('rg', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('estado_civil', models.CharField(max_length=10)),
                ('data_nasc', models.DateField()),
                ('cep', models.CharField(max_length=8)),
                ('endereco', models.CharField(max_length=200)),
                ('complemento', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=6)),
                ('cidade', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=60)),
                ('estado', models.CharField(max_length=40)),
                ('tipo_tel', models.CharField(max_length=10)),
                ('tel', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pessoa', models.CharField(max_length=200)),
                ('data_cadastro', models.DateField()),
                ('nome_fantasia', models.CharField(max_length=200)),
                ('razao_social', models.CharField(max_length=200)),
                ('cpf_cnpj', models.CharField(max_length=200)),
                ('rg_ie', models.CharField(max_length=200)),
                ('cep', models.CharField(max_length=200)),
                ('endereco', models.CharField(max_length=200)),
                ('numero', models.CharField(max_length=200)),
                ('cidade', models.CharField(max_length=200)),
                ('bairro', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('fax', models.CharField(max_length=200)),
                ('tel', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_produto', models.IntegerField()),
                ('cod_bar', models.CharField(max_length=200, unique=True)),
                ('data_cadastro', models.DateField()),
                ('descricao', models.CharField(max_length=200)),
                ('marca', models.CharField(max_length=200)),
                ('custo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('venda', models.DecimalField(decimal_places=2, max_digits=12)),
                ('lucro', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('estoque', models.PositiveIntegerField()),
            ],
        ),
    ]
