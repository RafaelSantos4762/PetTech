# Generated by Django 2.2.1 on 2019-10-27 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_pedido_efetivado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fornecedor_id', models.IntegerField()),
                ('fornece_nome', models.CharField(max_length=200)),
                ('produto_id', models.IntegerField()),
                ('quantidade', models.IntegerField()),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=12)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=150)),
            ],
        ),
    ]
